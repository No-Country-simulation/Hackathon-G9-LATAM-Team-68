(function () {
  var themeLink = document.getElementById("themeStylesheet");
  if (!themeLink) {
    return;
  }

  var selector = document.getElementById("themeSelector");
  var themes = {
    default: null,
    wireframe: themeLink.dataset.wireframe || themeLink.getAttribute("href"),
    modern: themeLink.dataset.modern,
    y2k: themeLink.dataset.y2k,
    hollow: themeLink.dataset.hollow
  };

  function applyTheme(themeName, persist) {
    if (!Object.prototype.hasOwnProperty.call(themes, themeName)) {
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
    document.dispatchEvent(new CustomEvent("team68:theme-change", { detail: { theme: themeName } }));

    if (persist) {
      localStorage.setItem("team68-theme", themeName);
    }
  }

  var storedTheme = localStorage.getItem("team68-theme");
  var initialTheme = Object.prototype.hasOwnProperty.call(themes, storedTheme) ? storedTheme : "default";

  applyTheme(initialTheme, false);

  if (selector) {
    selector.value = initialTheme;
    selector.addEventListener("change", function (event) {
      applyTheme(event.target.value, true);
    });
  }
})();
