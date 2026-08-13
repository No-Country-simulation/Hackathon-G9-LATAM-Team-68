(function () {
  function getBogotaISODate() {
    var formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/Bogota",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    });
    var parts = formatter.formatToParts(new Date());
    var dateObj = parts.reduce(function (acc, part) {
      acc[part.type] = part.value;
      return acc;
    }, {});

    return dateObj.year + "-" + dateObj.month + "-" + dateObj.day;
  }

  function showMessage(icon, title, text) {
    if (window.Swal) {
      window.Swal.fire({
        icon: icon,
        title: title,
        text: text,
        timer: icon === "success" ? 1600 : undefined,
        showConfirmButton: icon !== "success"
      });
      return;
    }

    alert(title + ": " + text);
  }

  function normalizeDate(input) {
    if (input) {
      return input;
    }

    return getBogotaISODate();
  }

  function setTodayOnInput(inputId) {
    var input = document.getElementById(inputId);
    if (!input) {
      return;
    }

    input.value = getBogotaISODate();
  }

  function setTodayOnDateFields() {
    document.querySelectorAll(".fecha-hoy").forEach(function (input) {
      input.value = getBogotaISODate();
    });
  }

  function renderRecentList(type, listId, emptyText) {
    if (!window.team68Movements) {
      return;
    }

    var list = document.getElementById(listId);
    if (!list) {
      return;
    }

    var rows = window.team68Movements.getAll()
      .filter(function (item) {
        return item.tipo === type;
      })
      .slice(0, 3);

    if (!rows.length) {
      list.innerHTML = "<li>" + emptyText + "</li>";
      return;
    }

    list.innerHTML = rows.map(function (row) {
      return "<li>" + window.team68Movements.formatDate(row.fecha) + " - " + row.concepto + " - " + window.team68Movements.formatAmount(row.monto) + "</li>";
    }).join("");
  }

  function renderRecentLists() {
    renderRecentList("Ingreso", "incomeRecentList", "Sin ingresos registrados");
    renderRecentList("Gasto", "expenseRecentList", "Sin gastos registrados");
  }

  function setupCreditInterestField() {
    var paymentMethod = document.getElementById("metodoPagoGasto");
    var interestWrapper = document.getElementById("tasaInteresGastoWrapper");
    var interestInput = document.getElementById("tasaInteresGasto");
    var conceptWrapper = document.getElementById("conceptoGastoWrapper");
    if (!paymentMethod || !interestWrapper || !interestInput || !conceptWrapper) {
      return;
    }

    function syncCreditInterestVisibility() {
      var isCredit = paymentMethod.value === "Credito";
      interestWrapper.classList.toggle("d-none", !isCredit);
      interestInput.required = isCredit;
      conceptWrapper.classList.toggle("col-md-12", !isCredit);
      conceptWrapper.classList.toggle("col-md-8", isCredit);

      if (!isCredit) {
        interestInput.value = "";
      }
    }

    paymentMethod.addEventListener("change", syncCreditInterestVisibility);
    syncCreditInterestVisibility();
  }

  function setupMovementForm(formId, saveBtnId, conceptoId, montoId, fechaId, categoriaId, metodoPagoId, tipo) {
    var form = document.getElementById(formId);
    var saveBtn = document.getElementById(saveBtnId);
    if (!form || !saveBtn || !window.team68Movements) {
      return;
    }

    saveBtn.addEventListener("click", async function () {
      var concepto = document.getElementById(conceptoId).value.trim().slice(0, 60);
      var monto = document.getElementById(montoId).value;
      var fecha = document.getElementById(fechaId).value;
      var categoriaNode = categoriaId ? document.getElementById(categoriaId) : null;
      var payload = {
        concepto: concepto,
        monto: Number(monto),
        fecha: normalizeDate(fecha),
        tipo: tipo
      };

      if (categoriaNode && categoriaNode.value) {
        payload.categoria = categoriaNode.value;
      }

      if (metodoPagoId) {
        payload.metodoPago = document.getElementById(metodoPagoId).value;
      }

      if (tipo === "Gasto") {
        var interestNode = document.getElementById("tasaInteresGasto");
        if (interestNode) {
          var interestRaw = String(interestNode.value || "").trim();
          if (payload.metodoPago === "Credito") {
            payload.tasaInteres = Number(interestRaw);
          }
        }
      }

      try {
        saveBtn.disabled = true;
        var row = await window.team68Movements.add(payload);
        form.reset();
        setTodayOnInput(fechaId);
        if (tipo === "Gasto") {
          var paymentMethod = document.getElementById("metodoPagoGasto");
          if (paymentMethod) {
            paymentMethod.dispatchEvent(new Event("change"));
          }
        }
        showMessage("success", tipo + " guardado", row.concepto + " por " + window.team68Movements.formatAmount(row.monto));
        renderRecentLists();
      } catch (error) {
        showMessage("error", "No se pudo guardar", error.message);
      } finally {
        saveBtn.disabled = false;
      }
    });
  }

  setupMovementForm("incomeEntryForm", "saveIncomeBtn", "conceptoIngreso", "montoIngreso", "fechaIngreso", "categoriaIngreso", null, "Ingreso");
  setupMovementForm("expenseEntryForm", "saveExpenseBtn", "conceptoGasto", "montoGasto", "fechaGasto", null, "metodoPagoGasto", "Gasto");
  setupCreditInterestField();
  setTodayOnDateFields();
  renderRecentLists();

  // Re-render when initial API synchronization finishes.
  document.addEventListener("team68:movements-updated", function () {
    renderRecentLists();
  });
})();