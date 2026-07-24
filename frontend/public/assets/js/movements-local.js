(function () {
  var STORAGE_KEY = "team68-movimientos";

  var seedMovements = [
    { id: 1, fecha: "2026-07-01", concepto: "Salario mensual", categoria: "Sueldo", tipo: "Ingreso", monto: 2400 },
    { id: 2, fecha: "2026-07-02", concepto: "Arriendo", categoria: "Vivienda", metodoPago: "Transferencia", tipo: "Gasto", monto: -650 },
    { id: 3, fecha: "2026-07-03", concepto: "Pago cliente landing page", categoria: "Freelance", tipo: "Ingreso", monto: 620 },
    { id: 4, fecha: "2026-07-04", concepto: "Gasolina", categoria: "Transporte", metodoPago: "Debito", tipo: "Gasto", monto: -58 },
    { id: 5, fecha: "2026-07-05", concepto: "Mercado quincenal", categoria: "Alimentacion", metodoPago: "Debito", tipo: "Gasto", monto: -145 },
    { id: 6, fecha: "2026-07-06", concepto: "Venta de accesorios", categoria: "Otros", tipo: "Ingreso", monto: 120 },
    { id: 7, fecha: "2026-07-07", concepto: "Consulta medica", categoria: "Salud", metodoPago: "Efectivo", tipo: "Gasto", monto: -95 },
    { id: 8, fecha: "2026-07-08", concepto: "Consultoria UX", categoria: "Freelance", tipo: "Ingreso", monto: 450 },
    { id: 9, fecha: "2026-07-09", concepto: "Curso online", categoria: "Educacion", metodoPago: "Credito", tipo: "Gasto", monto: -42 },
    { id: 10, fecha: "2026-07-10", concepto: "Interes bancario", categoria: "Otros", tipo: "Ingreso", monto: 36 },
    { id: 11, fecha: "2026-07-11", concepto: "Bus intermunicipal", categoria: "Transporte", metodoPago: "Efectivo", tipo: "Gasto", monto: -21 },
    { id: 12, fecha: "2026-07-12", concepto: "Plataforma de musica", categoria: "Subscripciones", metodoPago: "Credito", tipo: "Gasto", monto: -11 },
    { id: 13, fecha: "2026-07-13", concepto: "Clases particulares", categoria: "Otros", tipo: "Ingreso", monto: 90 },
    { id: 14, fecha: "2026-07-14", concepto: "Cena con amigos", categoria: "Entretenimiento", metodoPago: "Debito", tipo: "Gasto", monto: -72 },
    { id: 15, fecha: "2026-07-15", concepto: "Reembolso empresa", categoria: "Sueldo", tipo: "Ingreso", monto: 210 },
    { id: 16, fecha: "2026-07-16", concepto: "Corte de cabello", categoria: "Personal", metodoPago: "Efectivo", tipo: "Gasto", monto: -38 },
    { id: 17, fecha: "2026-07-17", concepto: "Diseno de logo", categoria: "Freelance", tipo: "Ingreso", monto: 300 },
    { id: 18, fecha: "2026-07-18", concepto: "Reserva de hotel", categoria: "Viajes", metodoPago: "Transferencia", tipo: "Gasto", monto: -180 },
    { id: 19, fecha: "2026-07-19", concepto: "Bono productividad", categoria: "Bono", tipo: "Ingreso", monto: 180 },
    { id: 20, fecha: "2026-07-20", concepto: "Compra de escritorio", categoria: "Otros", metodoPago: "Debito", tipo: "Gasto", monto: -85 }
  ];

  function parseStorage() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return null;
      }

      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : null;
    } catch (error) {
      return null;
    }
  }

  function saveStorage(movements) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(movements));
  }

  function ensureSeedData() {
    var existing = parseStorage();
    if (existing && existing.length) {
      return existing;
    }

    saveStorage(seedMovements);
    return seedMovements.slice();
  }

  function getMovements() {
    return ensureSeedData().slice().sort(function (a, b) {
      if (a.fecha === b.fecha) {
        return b.id - a.id;
      }

      return a.fecha < b.fecha ? 1 : -1;
    });
  }

  function saveMovements(movements) {
    saveStorage(movements);
  }

  function resetToSeedData() {
    var freshSeed = seedMovements.slice();
    saveMovements(freshSeed);
    return freshSeed;
  }

  function getNextId(movements) {
    if (!movements.length) {
      return 1;
    }

    return Math.max.apply(null, movements.map(function (entry) {
      return Number(entry.id || 0);
    })) + 1;
  }

  function addMovement(payload) {
    var concept = String(payload.concepto || "").trim();
    var amountValue = Number(payload.monto);
    var dateValue = String(payload.fecha || "").trim();
    var typeValue = payload.tipo === "Gasto" ? "Gasto" : "Ingreso";

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

    var rows = getMovements();
    var nextId = getNextId(rows);
    var normalizedAmount = typeValue === "Gasto" ? -Math.abs(amountValue) : Math.abs(amountValue);

    var entry = {
      id: nextId,
      fecha: dateValue,
      concepto: concept,
      categoria: String(payload.categoria || "Otros").trim() || "Otros",
      metodoPago: typeValue === "Gasto"
        ? (String(payload.metodoPago || "Efectivo").trim() || "Efectivo")
        : "",
      tipo: typeValue,
      monto: normalizedAmount
    };

    rows.push(entry);
    saveMovements(rows);
    return entry;
  }

  function formatDate(isoDate) {
    var parts = (isoDate || "").split("-");
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

    var rows = all.slice(0, 6);
    renderTable(summaryBody, rows, rowForSummary, 5);
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

  function attachEvents() {
    var applyFiltersBtn = document.getElementById("applyFiltersBtn");
    var clearFiltersBtn = document.getElementById("clearFiltersBtn");
    var resetFiltersBtn = document.getElementById("resetFiltersBtn");

    if (applyFiltersBtn) {
      applyFiltersBtn.addEventListener("click", loadHistoryTable);
    }

    if (clearFiltersBtn) {
      clearFiltersBtn.addEventListener("click", function () {
        var desde = document.getElementById("desde");
        var hasta = document.getElementById("hasta");
        var tipo = document.getElementById("tipo");
        var categoria = document.getElementById("categoria");

        if (desde) {
          desde.value = "";
        }

        if (hasta) {
          hasta.value = "";
        }

        if (tipo) {
          tipo.value = "Todos";
        }

        if (categoria) {
          categoria.value = "Todas";
        }

        loadHistoryTable();
      });
    }

    if (resetFiltersBtn) {
      resetFiltersBtn.addEventListener("click", function () {
        var confirmed = window.confirm("Esto restablecera los datos de ejemplo. Deseas continuar?");
        if (!confirmed) {
          return;
        }

        resetToSeedData();

        var desde = document.getElementById("desde");
        var hasta = document.getElementById("hasta");
        var tipo = document.getElementById("tipo");
        var categoria = document.getElementById("categoria");

        if (desde) {
          desde.value = "";
        }

        if (hasta) {
          hasta.value = "";
        }

        if (tipo) {
          tipo.value = "Todos";
        }

        if (categoria) {
          categoria.value = "Todas";
        }

        loadSummaryTable();
        loadHistoryTable();
      });
    }

  }

  window.team68Movements = {
    ensureSeedData: ensureSeedData,
    resetToSeedData: resetToSeedData,
    getAll: getMovements,
    add: addMovement,
    filter: filterMovements,
    formatDate: formatDate,
    formatAmount: formatAmount,
    reloadViews: function () {
      loadSummaryTable();
      loadHistoryTable();
    }
  };

  ensureSeedData();
  loadSummaryTable();
  loadHistoryTable();
  attachEvents();
})();
