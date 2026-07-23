(function () {
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

    return new Date().toISOString().slice(0, 10);
  }

  function renderRecentList(type, listId, emptyText) {
    if (!window.fintrackMovements) {
      return;
    }

    var list = document.getElementById(listId);
    if (!list) {
      return;
    }

    var rows = window.fintrackMovements.getAll()
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
        window.fintrackMovements.formatDate(row.fecha) +
        " - " + row.concepto +
        " - " + window.fintrackMovements.formatAmount(row.monto) +
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
    if (!form || !saveBtn || !window.fintrackMovements) {
      return;
    }

    saveBtn.addEventListener("click", function () {
      var concepto = document.getElementById("conceptoIngreso").value;
      var monto = document.getElementById("montoIngreso").value;
      var fecha = document.getElementById("fechaIngreso").value;
      var categoria = document.getElementById("categoriaIngreso").value;
      var cuenta = document.getElementById("cuentaIngreso").value;

      try {
        var row = window.fintrackMovements.add({
          concepto: concepto,
          monto: Number(monto),
          fecha: normalizeDate(fecha),
          categoria: categoria,
          cuenta: cuenta,
          tipo: "Ingreso"
        });

        form.reset();
        showMessage("success", "Ingreso guardado", row.concepto + " por " + window.fintrackMovements.formatAmount(row.monto));
        renderRecentLists();
      } catch (error) {
        showMessage("error", "No se pudo guardar", error.message);
      }
    });
  }

  function setupExpenseForm() {
    var form = document.getElementById("expenseEntryForm");
    var saveBtn = document.getElementById("saveExpenseBtn");
    if (!form || !saveBtn || !window.fintrackMovements) {
      return;
    }

    saveBtn.addEventListener("click", function () {
      var concepto = document.getElementById("conceptoGasto").value;
      var monto = document.getElementById("montoGasto").value;
      var fecha = document.getElementById("fechaGasto").value;
      var categoria = document.getElementById("categoriaGasto").value;
      var cuenta = document.getElementById("metodoPago").value;

      try {
        var row = window.fintrackMovements.add({
          concepto: concepto,
          monto: Number(monto),
          fecha: normalizeDate(fecha),
          categoria: categoria,
          cuenta: cuenta,
          tipo: "Gasto"
        });

        form.reset();
        showMessage("success", "Gasto guardado", row.concepto + " por " + window.fintrackMovements.formatAmount(row.monto));
        renderRecentLists();
      } catch (error) {
        showMessage("error", "No se pudo guardar", error.message);
      }
    });
  }

  setupIncomeForm();
  setupExpenseForm();
  renderRecentLists();
})();

const hoy = new Date().toISOString().split('T')[0];

document.querySelectorAll('.fecha-hoy').forEach(input => {
    input.value = hoy;
});