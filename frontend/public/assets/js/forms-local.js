(function () {
  function getBogotaISODate() {
    var formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/Bogota",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    });
    var parts = formatter.formatToParts(new Date());
    var year = "";
    var month = "";
    var day = "";

    parts.forEach(function (part) {
      if (part.type === "year") {
        year = part.value;
      }

      if (part.type === "month") {
        month = part.value;
      }

      if (part.type === "day") {
        day = part.value;
      }
    });

    return year + "-" + month + "-" + day;
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
      return "<li>" +
        window.team68Movements.formatDate(row.fecha) +
        " - " + row.concepto +
        " - " + window.team68Movements.formatAmount(row.monto) +
        "</li>";
    }).join("");
  }

  function renderRecentLists() {
    renderRecentList("Ingreso", "incomeRecentList", "Sin ingresos registrados");
    renderRecentList("Gasto", "expenseRecentList", "Sin gastos registrados");
  }

  function setupIncomeForm() {
    var form = document.getElementById("incomeEntryForm");
    var saveBtn = document.getElementById("saveIncomeBtn");
    if (!form || !saveBtn || !window.team68Movements) {
      return;
    }

    saveBtn.addEventListener("click", function () {
      var concepto = document.getElementById("conceptoIngreso").value;
      var monto = document.getElementById("montoIngreso").value;
      var fecha = document.getElementById("fechaIngreso").value;
      var categoria = document.getElementById("categoriaIngreso").value;


      try {
        var row = window.team68Movements.add({
          concepto: concepto,
          monto: Number(monto),
          fecha: normalizeDate(fecha),
          categoria: categoria,
          tipo: "Ingreso"
        });

        form.reset();
        setTodayOnInput("fechaIngreso");
        showMessage("success", "Ingreso guardado", row.concepto + " por " + window.team68Movements.formatAmount(row.monto));
        renderRecentLists();
      } catch (error) {
        showMessage("error", "No se pudo guardar", error.message);
      }
    });
  }

  function setupExpenseForm() {
    var form = document.getElementById("expenseEntryForm");
    var saveBtn = document.getElementById("saveExpenseBtn");
    if (!form || !saveBtn || !window.team68Movements) {
      return;
    }

    saveBtn.addEventListener("click", function () {
      var concepto = document.getElementById("conceptoGasto").value.trim().slice(0, 60);
      var monto = document.getElementById("montoGasto").value;
      var fecha = document.getElementById("fechaGasto").value;
      var categoria = document.getElementById("categoriaGasto").value;
      var metodoPago = document.getElementById("metodoPagoGasto").value;

      try {
        var row = window.team68Movements.add({
          concepto: concepto,
          monto: Number(monto),
          fecha: normalizeDate(fecha),
          categoria: categoria,
          metodoPago: metodoPago,
          tipo: "Gasto"
        });

        form.reset();
        setTodayOnInput("fechaGasto");
        showMessage("success", "Gasto guardado", row.concepto + " por " + window.team68Movements.formatAmount(row.monto));
        renderRecentLists();
      } catch (error) {
        showMessage("error", "No se pudo guardar", error.message);
      }
    });
  }

  setupIncomeForm();
  setupExpenseForm();
  setTodayOnDateFields();
  renderRecentLists();
})();