(function () {
  var PROFILE_KEY = "team68-financial-profile";
  var CATEGORY_TO_API = {
    Vivienda: "VIVIENDA",
    Alimentacion: "ALIMENTACION",
    Transporte: "TRANSPORTE",
    Salud: "SALUD",
    Educacion: "EDUCACION",
    Entretenimiento: "ENTRETENIMIENTO",
    Subscripciones: "SUSCRIPCIONES",
    Personal: "COMPRAS_PERSONALES",
    Viajes: "VIAJES",
    Otros: "OTROS",
    Sueldo: "OTROS",
    Bono: "OTROS",
    Freelance: "OTROS"
  };
  var CATEGORY_FROM_API = {
    VIVIENDA: "Vivienda",
    ALIMENTACION: "Alimentacion",
    TRANSPORTE: "Transporte",
    SALUD: "Salud",
    EDUCACION: "Educacion",
    ENTRETENIMIENTO: "Entretenimiento",
    SUSCRIPCIONES: "Subscripciones",
    COMPRAS_PERSONALES: "Personal",
    VIAJES: "Viajes",
    OTROS: "Otros"
  };
  var syncPopupTimer = null;

  function showMessage(icon, title, text) {
    if (window.Swal) {
      window.Swal.fire({
        icon: icon,
        title: title,
        text: text
      });
      return;
    }

    alert(title + ": " + text);
  }

  function showSyncPopup(state, message) {
    var text = message || "Movimientos actualizados.";
    var icon = "info";

    if (state === "success") {
      icon = "success";
    } else if (state === "error") {
      icon = "error";
    }

    if (window.Swal) {
      window.Swal.fire({
        toast: true,
        position: "top-end",
        icon: icon,
        title: text,
        showConfirmButton: false,
        timer: state === "loading" ? 1200 : 1800,
        timerProgressBar: true
      });
      return;
    }

    var popup = document.getElementById("team68-sync-toast");
    if (!popup) {
      popup = document.createElement("div");
      popup.id = "team68-sync-toast";
      popup.setAttribute("role", "status");
      popup.style.position = "fixed";
      popup.style.top = "16px";
      popup.style.right = "16px";
      popup.style.zIndex = "1080";
      popup.style.padding = "10px 12px";
      popup.style.borderRadius = "8px";
      popup.style.color = "#fff";
      popup.style.fontSize = "0.875rem";
      popup.style.boxShadow = "0 8px 20px rgba(0, 0, 0, 0.2)";
      popup.style.display = "none";
      document.body.appendChild(popup);
    }

    popup.style.background = state === "error" ? "#dc3545" : (state === "success" ? "#198754" : "#0d6efd");

    popup.textContent = text;
    popup.style.display = "block";

    if (syncPopupTimer) {
      window.clearTimeout(syncPopupTimer);
    }

    syncPopupTimer = window.setTimeout(function () {
      popup.style.display = "none";
    }, state === "loading" ? 1200 : 1800);
  }

  function setSyncStatus(state, message) {
    if (state === "idle") {
      return;
    }

    if (state === "loading") {
      showSyncPopup("loading", message || "Sincronizando movimientos con la API...");
      return;
    }

    if (state === "success") {
      showSyncPopup("success", message || "Movimientos actualizados desde la API.");
      return;
    }

    if (state === "error") {
      showSyncPopup("error", message || "No se pudo sincronizar con la API.");
    }
  }

  function normalizePayment(value) {
    var text = String(value || "").toLowerCase();
    if (text.indexOf("credit") >= 0) {
      return "Credito";
    }
    if (text.indexOf("debit") >= 0) {
      return "Debito";
    }
    if (text.indexOf("transfer") >= 0) {
      return "Transferencia";
    }
    if (text.indexOf("efect") >= 0 || !text) {
      return "Efectivo";
    }

    return String(value || "Efectivo");
  }

  function mapCategoryToApi(value) {
    var key = String(value || "Otros").trim();
    return CATEGORY_TO_API[key] || "OTROS";
  }

  function mapCategoryFromApi(value) {
    var key = String(value || "OTROS").trim().toUpperCase();
    return CATEGORY_FROM_API[key] || "Otros";
  }

  function sortRows(rows) {
    return rows.slice().sort(function (a, b) {
      if (a.fecha === b.fecha) {
        return String(b.id).localeCompare(String(a.id));
      }

      return a.fecha < b.fecha ? 1 : -1;
    });
  }

  function buildIngresoRow(item) {
    return {
      id: item.id || "ing-" + item.fecha + "-" + item.descripcion,
      fecha: item.fecha,
      concepto: item.descripcion || "Ingreso",
      categoria: "Sueldo",
      metodoPago: "",
      tipo: "Ingreso",
      monto: Math.abs(Number(item.monto || 0))
    };
  }

  function buildExpenseRow(item) {
    return {
      id: item.id || "gas-" + item.fecha + "-" + item.descripcion,
      fecha: item.fecha,
      concepto: item.descripcion || "Gasto",
      categoria: mapCategoryFromApi(item.categoria),
      metodoPago: normalizePayment(item.formaPago || item.forma_pago),
      tipo: "Gasto",
      monto: -Math.abs(Number(item.monto || 0)),
      tasaInteres: Number(item.tasaDeInteresDeLaTarjeta || item.tasa_de_interes_de_la_tarjeta || 0)
    };
  }

  function getUniqueRows(rows) {
    var byId = {};
    rows.forEach(function (row) {
      byId[String(row.id)] = row;
    });
    return Object.keys(byId).map(function (id) {
      return byId[id];
    });
  }

  var movementCache = [];

  function getMovements() {
    return sortRows(movementCache);
  }

  function setMovements(rows) {
    movementCache = sortRows(getUniqueRows(rows));
  }

  function upsertMovement(row) {
    var next = movementCache.filter(function (item) {
      return String(item.id) !== String(row.id);
    });
    next.push(row);
    setMovements(next);
  }

  function formatDate(isoDate) {
    var parts = String(isoDate || "").split("-");
    if (parts.length !== 3) {
      return isoDate || "-";
    }

    return parts[2] + "/" + parts[1] + "/" + parts[0];
  }

  function formatAmount(value) {
    var amount = Number(value || 0);
    var sign = amount >= 0 ? "+$" : "-$";
    return sign + Math.abs(amount).toLocaleString("es-ES");
  }

  function formatCardAmount(value) {
    var amount = Number(value || 0);
    if (amount < 0) {
      return "-$" + Math.abs(amount).toLocaleString("es-ES");
    }

    return "$" + amount.toLocaleString("es-ES");
  }

  function calculateTotals(rows) {
    return rows.reduce(function (acc, item) {
      var amount = Number(item.monto || 0);
      if (amount >= 0) {
        acc.income += amount;
      } else {
        acc.expense += Math.abs(amount);
      }

      return acc;
    }, { income: 0, expense: 0 });
  }

  function setBalanceStateClass(node, balance) {
    if (!node) {
      return;
    }

    node.classList.remove("total-positive", "total-negative", "total-neutral");

    if (balance > 0) {
      node.classList.add("total-positive");
      return;
    }

    if (balance < 0) {
      node.classList.add("total-negative");
      return;
    }

    node.classList.add("total-neutral");
  }

  function renderSummaryTotals(rows) {
    var incomeNode = document.getElementById("summaryIncomeTotal");
    var expenseNode = document.getElementById("summaryExpenseTotal");
    var balanceNode = document.getElementById("summaryBalanceTotal");
    if (!incomeNode || !expenseNode || !balanceNode) {
      return;
    }

    var totals = calculateTotals(rows);
    var balance = totals.income - totals.expense;

    incomeNode.textContent = formatCardAmount(totals.income);
    expenseNode.textContent = formatCardAmount(totals.expense);
    balanceNode.textContent = formatCardAmount(balance);
    setBalanceStateClass(balanceNode, balance);
  }

  function renderHistoryTotals(rows) {
    var incomeNode = document.getElementById("historyIncomeTotal");
    var expenseNode = document.getElementById("historyExpenseTotal");
    var balanceNode = document.getElementById("historyBalanceTotal");
    if (!incomeNode || !expenseNode || !balanceNode) {
      return;
    }

    var totals = calculateTotals(rows);
    var balance = totals.income - totals.expense;

    incomeNode.textContent = formatCardAmount(totals.income);
    expenseNode.textContent = formatCardAmount(totals.expense);
    balanceNode.textContent = formatCardAmount(balance);
    setBalanceStateClass(balanceNode, balance);
  }

  function rowForSummary(item) {
    return "<tr>" +
      "<td>" + formatDate(item.fecha) + "</td>" +
      "<td>" + item.concepto + "</td>" +
      "<td>" + item.categoria + "</td>" +
      "<td>" + item.tipo + "</td>" +
      '<td class="text-end">' + formatAmount(item.monto) + "</td>" +
      "</tr>";
  }

  function rowForHistory(item) {
    var metodoPago = item.tipo === "Gasto" ? (item.metodoPago || "") : "";

    return "<tr>" +
      "<td>" + formatDate(item.fecha) + "</td>" +
      "<td>" + item.concepto + "</td>" +
      "<td>" + item.categoria + "</td>" +
      "<td>" + metodoPago + "</td>" +
      "<td>" + item.tipo + "</td>" +
      '<td class="text-end">' + formatAmount(item.monto) + "</td>" +
      "</tr>";
  }

  function renderTable(tbody, rows, rowRenderer, emptyColspan) {
    if (!tbody) {
      return;
    }

    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="' + emptyColspan + '" class="text-center">Sin registros</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map(rowRenderer).join("");
  }

  function getFilters() {
    var fromInput = document.getElementById("desde");
    var toInput = document.getElementById("hasta");
    var typeSelect = document.getElementById("tipo");
    var categorySelect = document.getElementById("categoria");

    return {
      desde: fromInput ? fromInput.value : "",
      hasta: toInput ? toInput.value : "",
      tipo: typeSelect ? typeSelect.value : "Todos",
      categoria: categorySelect ? categorySelect.value : "Todas"
    };
  }

  function filterMovements(movements, filters) {
    return movements.filter(function (item) {
      if (filters.tipo && filters.tipo !== "Todos" && item.tipo !== filters.tipo) {
        return false;
      }

      if (filters.categoria && filters.categoria !== "Todas" && item.categoria !== filters.categoria) {
        return false;
      }

      if (filters.desde && item.fecha < filters.desde) {
        return false;
      }

      if (filters.hasta && item.fecha > filters.hasta) {
        return false;
      }

      return true;
    });
  }

  function loadSummaryTable() {
    var summaryBody = document.getElementById("summaryMovementsBody");
    var all = getMovements();

    renderSummaryTotals(all);

    if (!summaryBody) {
      return;
    }

    renderTable(summaryBody, all.slice(0, 6), rowForSummary, 5);
  }

  function loadHistoryTable() {
    var historyBody = document.getElementById("historyMovementsBody");
    var all = getMovements();
    var rows = filterMovements(all, getFilters());

    renderHistoryTotals(rows);

    document.dispatchEvent(new CustomEvent("team68:history-data-change", {
      detail: {
        rows: rows
      }
    }));

    if (!historyBody) {
      return;
    }

    renderTable(historyBody, rows, rowForHistory, 6);
  }

  function getAnalysisPayload(rows) {
    var session = window.team68Api ? window.team68Api.getSession() : null;
    if (!session || !session.id) {
      return null;
    }

    var validDates = rows.map(function (item) {
      return item.fecha;
    }).filter(function (date) {
      return /^\d{4}-\d{2}-\d{2}$/.test(String(date || ""));
    }).sort();

    var today = new Date().toISOString().slice(0, 10);
    var periodStart = validDates.length ? validDates[0] : today;
    var periodEnd = validDates.length ? validDates[validDates.length - 1] : today;

    return {
      usuario: {
        id: session.id,
        nombre: session.nombre || session.username || "Usuario"
      },
      periodo: {
        inicio: periodStart,
        fin: periodEnd
      },
      ingresos: rows.filter(function (item) {
        return item.tipo === "Ingreso";
      }).map(function (item) {
        return {
          fecha: item.fecha,
          descripcion: item.concepto,
          monto: Math.abs(Number(item.monto || 0))
        };
      }),
      transacciones: rows.filter(function (item) {
        return item.tipo === "Gasto";
      }).map(function (item) {
        var payload = {
          fecha: item.fecha,
          descripcion: item.concepto,
          monto: Math.abs(Number(item.monto || 0)),
          tipoFinanciero: "CONSUMO",
          categoria: mapCategoryToApi(item.categoria),
          forma_pago: normalizePayment(item.metodoPago)
        };

        if (normalizePayment(item.metodoPago) === "Credito") {
          var interest = Number(item.tasaInteres || 0);
          if (Number.isFinite(interest) && interest > 0) {
            payload.tasa_de_interes_de_la_tarjeta = interest;
          }
        }

        return payload;
      })
    };
  }

  async function refreshFinancialProfile(rows) {
    if (!window.team68Api || !window.team68Api.isAuthenticated()) {
      return;
    }

    var payload = getAnalysisPayload(rows);
    if (!payload) {
      return;
    }

    try {
      var profile = await window.team68Api.realizarAnalisis(payload);
      localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
      document.dispatchEvent(new CustomEvent("team68:profile-updated", {
        detail: {
          profile: profile
        }
      }));
    } catch (error) {
      localStorage.removeItem(PROFILE_KEY);
      document.dispatchEvent(new CustomEvent("team68:profile-updated", {
        detail: {
          profile: null
        }
      }));
      setSyncStatus("error", "No se pudo actualizar el analisis de perfil.");
    }
  }

  async function syncFromApi(options) {
    var config = options || {};

    if (!window.team68Api || !window.team68Api.isAuthenticated()) {
      return getMovements();
    }

    var usuarioId = window.team68Api.getUsuarioId();
    setSyncStatus("loading");

    try {
      var responses = await Promise.all([
        window.team68Api.getIngresosUsuario(usuarioId),
        window.team68Api.getMovimientosUsuario(usuarioId)
      ]);
      var ingresos = Array.isArray(responses[0]) ? responses[0] : [];
      var gastos = Array.isArray(responses[1]) ? responses[1] : [];
      var mergedRows = ingresos.map(buildIngresoRow).concat(gastos.map(buildExpenseRow));

      setMovements(mergedRows);
      loadSummaryTable();
      loadHistoryTable();
      await refreshFinancialProfile(getMovements());

      document.dispatchEvent(new CustomEvent("team68:movements-updated", {
        detail: {
          rows: getMovements()
        }
      }));

      setSyncStatus("success");

      return getMovements();
    } catch (error) {
      setSyncStatus("error", "No se pudo sincronizar con la API: " + error.message);
      setMovements([]);
      loadSummaryTable();
      loadHistoryTable();
      localStorage.removeItem(PROFILE_KEY);
      document.dispatchEvent(new CustomEvent("team68:profile-updated", {
        detail: {
          profile: null
        }
      }));
      if (!config.silent) {
        showMessage("error", "No se pudieron cargar los movimientos", error.message);
      }

      throw error;
    }
  }

  function validatePayload(payload) {
    var concept = String(payload.concepto || "").trim();
    var amountValue = Number(payload.monto);
    var dateValue = String(payload.fecha || "").trim();

    if (!concept) {
      throw new Error("El concepto es obligatorio.");
    }

    if (concept.length > 60) {
      throw new Error("El concepto no puede superar los 60 caracteres.");
    }

    if (!dateValue) {
      throw new Error("La fecha es obligatoria.");
    }

    if (!Number.isFinite(amountValue) || amountValue <= 0) {
      throw new Error("El monto debe ser mayor a 0.");
    }

    return {
      concepto: concept,
      monto: amountValue,
      fecha: dateValue,
      categoria: String(payload.categoria || "Otros").trim() || "Otros",
      metodoPago: normalizePayment(payload.metodoPago),
      tipo: payload.tipo === "Gasto" ? "Gasto" : "Ingreso",
      tasaInteres: Number(payload.tasaInteres || 0)
    };
  }

  async function addMovement(payload) {
    if (!window.team68Api || !window.team68Api.isAuthenticated()) {
      throw new Error("Debes iniciar sesion para registrar movimientos.");
    }

    var normalized = validatePayload(payload);
    var usuarioId = window.team68Api.getUsuarioId();
    setSyncStatus("loading", "Guardando movimiento en la API...");

    try {
      if (normalized.tipo === "Ingreso") {
        var incomePayload = {
          fecha: normalized.fecha,
          descripcion: normalized.concepto,
          monto: Math.abs(normalized.monto)
        };
        var incomeResponse = await window.team68Api.crearIngreso(usuarioId, incomePayload);
        var incomeRow = buildIngresoRow(incomeResponse || incomePayload);
        upsertMovement(incomeRow);
        loadSummaryTable();
        loadHistoryTable();
        refreshFinancialProfile(getMovements());
        setSyncStatus("success", "Movimiento guardado y sincronizado.");
        return incomeRow;
      }

      if (normalized.metodoPago === "Credito") {
        if (!Number.isFinite(normalized.tasaInteres) || normalized.tasaInteres <= 0) {
          throw new Error("La tasa de interes es obligatoria cuando el metodo de pago es Credito.");
        }
      }

      var expensePayload = {
        fecha: normalized.fecha,
        descripcion: normalized.concepto,
        monto: Math.abs(normalized.monto),
        tipoFinanciero: "CONSUMO",
        forma_pago: normalized.metodoPago
      };

      if (normalized.metodoPago === "Credito") {
        expensePayload.tasa_de_interes_de_la_tarjeta = normalized.tasaInteres;
      }

      var expenseResponse = await window.team68Api.crearTransaccion(usuarioId, expensePayload);
      var expenseRow = buildExpenseRow(expenseResponse || expensePayload);
      if (!expenseRow.id) {
        expenseRow.id = "gas-" + Date.now();
      }
      upsertMovement(expenseRow);
      loadSummaryTable();
      loadHistoryTable();
      refreshFinancialProfile(getMovements());
      setSyncStatus("success", "Movimiento guardado y sincronizado.");
      return expenseRow;
    } catch (error) {
      setSyncStatus("error", "No se pudo guardar en la API: " + error.message);
      throw error;
    }
  }

  function attachEvents() {
    var applyFiltersBtn = document.getElementById("applyFiltersBtn");
    var clearFiltersBtn = document.getElementById("clearFiltersBtn");

    if (applyFiltersBtn) {
      applyFiltersBtn.addEventListener("click", loadHistoryTable);
    }

    if (clearFiltersBtn) {
      clearFiltersBtn.addEventListener("click", function () {
        var resetFields = {"desde": "", "hasta": "", "tipo": "Todos", "categoria": "Todas"};
        Object.keys(resetFields).forEach(function (id) {
          var el = document.getElementById(id);
          if (el) {
            el.value = resetFields[id];
          }
        });
        loadHistoryTable();
      });
    }

  }


  window.team68Movements = {
    getAll: getMovements,
    add: addMovement,
    filter: filterMovements,
    formatDate: formatDate,
    formatAmount: formatAmount,
    sync: syncFromApi,
    reloadViews: function () {
      loadSummaryTable();
      loadHistoryTable();
    }
  };

  if (!window.team68Api || !window.team68Api.requireAuth()) {
    return;
  }

  loadSummaryTable();
  loadHistoryTable();
  attachEvents();
  setSyncStatus("loading");

  syncFromApi({
    silent: true
  }).catch(function () {
    // API-only mode: if sync fails there is no local fallback for records.
  });
})();
