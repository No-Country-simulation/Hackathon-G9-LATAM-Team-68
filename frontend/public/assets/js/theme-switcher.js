(function () {
  var hasOwn = Object.prototype.hasOwnProperty.call.bind(Object.prototype.hasOwnProperty);

  var themeLink = document.getElementById("themeStylesheet");
  if (!themeLink) {
    return;
  }

  var selector = document.getElementById("themeSelector");
  var apiConnectedFieldIds = {
    user: true,
    password: true,
    fechaIngreso: true,
    montoIngreso: true,
    conceptoIngreso: true,
    categoriaIngreso: true,
    fechaGasto: true,
    montoGasto: true,
    metodoPagoGasto: true,
    conceptoGasto: true,
    tasaInteresGasto: true
  };
  var themes = {
    default: null,
    y2k: themeLink.dataset.y2k,
    hollow: themeLink.dataset.hollow,
    rendi: themeLink.dataset.rendi
  };

  function applyApiInteractionMarkers(themeName) {
    var fields = document.querySelectorAll("main input, main select, main textarea");
    if (!fields.length) {
      return;
    }

    fields.forEach(function (field) {
      field.classList.remove("wf-api-on", "wf-api-off");

      if (themeName !== "default") {
        return;
      }

      if (apiConnectedFieldIds[field.id]) {
        field.classList.add("wf-api-on");
      } else {
        field.classList.add("wf-api-off");
      }
    });
  }

  function applyTheme(themeName, persist) {
    if (!hasOwn(themes, themeName)) {
      return;
    }

    if (themes[themeName]) {
      themeLink.disabled = false;
      themeLink.setAttribute("href", themes[themeName]);
    } else {
      themeLink.disabled = true;
      themeLink.setAttribute("href", "");
    }

    document.documentElement.setAttribute("data-theme", themeName);
    applyApiInteractionMarkers(themeName);
    document.dispatchEvent(new CustomEvent("team68:theme-change", { detail: { theme: themeName } }));

    if (persist) {
      localStorage.setItem("team68-theme", themeName);
    }
  }

  var storedTheme = localStorage.getItem("team68-theme");
  var initialTheme = hasOwn(themes, storedTheme) ? storedTheme : "rendi";

  applyTheme(initialTheme, false);

  if (selector) {
    selector.value = initialTheme;
    selector.addEventListener("change", function (event) {
      applyTheme(event.target.value, true);
    });
  }
})();
