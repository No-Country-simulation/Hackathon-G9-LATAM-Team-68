(function () {
  if (typeof introJs !== "function") {
    return;
  }

  var trigger = document.getElementById("pageHelpTrigger");
  if (!trigger) {
    return;
  }

  var currentPage = window.location.pathname.split("/").pop() || "";
  var pageTours = {
    "login.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la página",
        intro: "Abre esta guia en cualquier momento para recordar que hace cada bloque."
      },
      {
        element: "#loginCard",
        title: "Acceso",
        intro: "Completa tu usuario y contraseña para entrar al panel principal."
      },
      {
        element: "#user",
        title: "Usuario",
        intro: "Usa este campo para escribir la cuenta con la que deseas ingresar."
      },
      {
        element: "#password",
        title: "Contrasena",
        intro: "Aquí introduces tu contraseña antes de pulsar Ingresar."
      }
    ],
    "summary.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la página",
        intro: "Activa este recorrido para ubicar rápidamente las secciones del resumen."
      },
      {
        element: "#summaryHeader",
        title: "Resumen mensual",
        intro: "Aquí ves el período actual y los accesos para crear movimientos nuevos."
      },
      {
        element: "#summaryTotals",
        title: "Indicadores clave",
        intro: "Estas tarjetas muestran ingresos, gastos y balance acumulado del mes."
      },
      {
        element: "#summaryMovements",
        title: "Últimos movimientos",
        intro: "La tabla resume las transacciones recientes para una revisión rápida."
      }
    ],
    "income.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la página",
        intro: "Usa esta ayuda para identificar el flujo de carga de ingresos."
      },
      {
        element: "#incomeForm",
        title: "Formulario de ingreso",
        intro: "Registra fecha, monto y concepto que deseas guardar."
      },
      {
        element: "#incomeRecent",
        title: "Ingresos recientes",
        intro: "Este bloque muestra ejemplos de los últimos ingresos cargados."
      }
    ],
    "expense.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la página",
        intro: "Este recorrido explica donde registrar y revisar gastos."
      },
      {
        element: "#expenseForm",
        title: "Formulario de gasto",
        intro: "Aquí capturas la fecha, monto, método de pago del gasto y concepto."
      },
      {
        element: "#expenseRecent",
        title: "Gastos recientes",
        intro: "Este listado sirve como referencia rápida de los últimos egresos registrados."
      }
    ],
    "history.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la página",
        intro: "Desde aquí puedes revisar cómo filtrar y analizar el historial."
      },
      {
        element: "#historyFilters",
        title: "Filtros",
        intro: "Define rango de fechas, tipo y categoría para acotar el historial."
      },
      {
        element: "#historyTotals",
        title: "Indicadores clave",
        intro: "Estas tarjetas muestran ingresos, gastos y balance filtrados."
      },
      {
        element: "#historyChartCard",
        title: "Analitica visual",
        intro: "La gráfica agrupa gastos por categoría para detectar tendencias rápidamente."
      },
      {
        element: "#historyResults",
        title: "Resultados",
        intro: "La tabla central muestra los movimientos que cumplen los filtros seleccionados."
      }
    ],
    "perfil.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la página",
        intro: "Este recorrido te explica cómo leer los indicadores de salud financiera."
      },
      {
        element: "#financialHealthHeader",
        title: "Resumen de estado",
        intro: "Esta cabecera presenta el objetivo de la vista y acceso al historial completo."
      },
      {
        element: "#financialHealthMetrics",
        title: "Indicadores porcentuales",
        intro: "Aquí se muestran salud financiera, endeudamiento y ahorro con gráficas de pastel."
      },
      {
        element: "#medallasObtenidas",
        title: "Medallas obtenidas",
        intro: "Aquí se muestran las medallas que has obtenido por tus logros financieros."
      }
    ]
  };

  function buildSteps(definition) {
    return definition.map(function (step) {
      if (!step.element) {
        return step;
      }
      var element = document.querySelector(step.element);
      return element ? {
        element: element,
        title: step.title,
        intro: step.intro
      } : null;
    }).filter(Boolean);
  }

  function applyCloseIcon() {
    var skipButton = document.querySelector(".introjs-skipbutton");
    if (!skipButton) {
      return;
    }

    skipButton.setAttribute("aria-label", "Cerrar ayuda");
    skipButton.innerHTML = 'X<span class="visually-hidden">Cerrar ayuda</span>';
  }

  function startHelp() {
    var steps = buildSteps(pageTours[currentPage] || []);
    if (!steps.length) {
      steps = [{
        title: "Ayuda",
        intro: "No hay instrucciones configuradas para esta página todavía."
      }];
    }

    var tour = introJs.tour().setOptions({
      steps: steps,
      nextLabel: "Siguiente",
      prevLabel: "Anterior",
      doneLabel: "Cerrar",
      skipLabel: "",
      showProgress: true,
      showBullets: false,
      exitOnOverlayClick: true
    });

    tour.onafterchange(applyCloseIcon);
    tour.onchange(applyCloseIcon);
    tour.start();
    requestAnimationFrame(applyCloseIcon);
  }

  trigger.addEventListener("click", startHelp);
})();