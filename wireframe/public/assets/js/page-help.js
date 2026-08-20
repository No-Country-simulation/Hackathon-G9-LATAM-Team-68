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
        title: "Ayuda de la pagina",
        intro: "Abre esta guia en cualquier momento para recordar que hace cada bloque."
      },
      {
        element: "#loginCard",
        title: "Acceso",
        intro: "Completa tu correo y contrasena para entrar al panel principal."
      },
      {
        element: "#email",
        title: "Correo",
        intro: "Usa este campo para escribir la cuenta con la que deseas ingresar."
      },
      {
        element: "#password",
        title: "Contrasena",
        intro: "Aqui introduces tu contrasena antes de pulsar Ingresar."
      }
    ],
    "welcome.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la pagina",
        intro: "Esta visita guiada resume los accesos rapidos de la maqueta."
      },
      {
        element: "#welcomeHero",
        title: "Vista general",
        intro: "La portada resume el objetivo de la app y te lleva a los flujos principales."
      },
      {
        element: "#welcomeActions",
        title: "Acciones rapidas",
        intro: "Desde aqui puedes ir al resumen o abrir directamente los formularios de ingresos y gastos."
      },
      {
        element: "#welcomeModules",
        title: "Modulos previstos",
        intro: "Esta tarjeta enumera los modulos contemplados en el wireframe."
      }
    ],
    "summary.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la pagina",
        intro: "Activa este recorrido para ubicar rapidamente las secciones del resumen."
      },
      {
        element: "#summaryHeader",
        title: "Resumen mensual",
        intro: "Aqui ves el periodo actual y los accesos para crear movimientos nuevos."
      },
      {
        element: "#summaryTotals",
        title: "Indicadores clave",
        intro: "Estas tarjetas muestran ingresos, gastos y balance acumulado del mes."
      },
      {
        element: "#summaryMovements",
        title: "Ultimos movimientos",
        intro: "La tabla resume las transacciones recientes para una revision rapida."
      }
    ],
    "income.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la pagina",
        intro: "Usa esta ayuda para identificar el flujo de carga de ingresos."
      },
      {
        element: "#incomeForm",
        title: "Formulario de ingreso",
        intro: "Registra concepto, monto, fecha y cuenta del ingreso que deseas guardar."
      },
      {
        element: "#cuentaIngreso",
        title: "Cuenta de destino",
        intro: "Selecciona donde impacta el dinero para mantener el control de tus fondos."
      },
      {
        element: "#incomeRecent",
        title: "Ingresos recientes",
        intro: "Este bloque muestra ejemplos de los ultimos ingresos cargados."
      }
    ],
    "expense.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la pagina",
        intro: "Este recorrido explica donde registrar y revisar gastos."
      },
      {
        element: "#expenseForm",
        title: "Formulario de gasto",
        intro: "Aqui capturas el concepto, categoria, monto y metodo de pago del gasto."
      },
      {
        element: "#metodoPago",
        title: "Metodo de pago",
        intro: "Indica si el gasto se hizo con tarjeta, transferencia o efectivo."
      },
      {
        element: "#expenseRecent",
        title: "Gastos recientes",
        intro: "Este listado sirve como referencia rapida de los ultimos egresos registrados."
      }
    ],
    "history.html": [
      {
        element: "#pageHelpTrigger",
        title: "Ayuda de la pagina",
        intro: "Desde aqui puedes revisar como filtrar y analizar el historial."
      },
      {
        element: "#historyFilters",
        title: "Filtros",
        intro: "Define rango de fechas, tipo y categoria para acotar el historial."
      },
      {
        element: "#historyResults",
        title: "Resultados",
        intro: "La tabla central muestra los movimientos que cumplen los filtros seleccionados."
      },
      {
        element: "#historyChartCard",
        title: "Analitica visual",
        intro: "La grafica agrupa gastos por categoria para detectar tendencias rapidamente."
      }
    ]
  };

  function buildSteps(definition) {
    return definition.filter(function (step) {
      return !step.element || document.querySelector(step.element);
    }).map(function (step) {
      if (!step.element) {
        return step;
      }

      return {
        element: document.querySelector(step.element),
        title: step.title,
        intro: step.intro
      };
    });
  }

  function applyCloseIcon() {
    var skipButton = document.querySelector(".introjs-skipbutton");
    if (!skipButton) {
      return;
    }

    skipButton.setAttribute("aria-label", "Cerrar ayuda");
    skipButton.innerHTML = '<ion-icon name="close-outline" aria-hidden="true"></ion-icon><span class="visually-hidden">Cerrar ayuda</span>';
  }

  function startHelp() {
    var steps = buildSteps(pageTours[currentPage] || []);
    if (!steps.length) {
      steps = [{
        title: "Ayuda",
        intro: "No hay instrucciones configuradas para esta pagina todavia."
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