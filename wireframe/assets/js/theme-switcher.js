(function () {
  var themeLink = document.getElementById("themeStylesheet");
  if (!themeLink) {
    return;
  }

  var selector = document.getElementById("themeSelector");
  var themes = {
    wireframe: themeLink.dataset.wireframe || themeLink.getAttribute("href"),
    modern: themeLink.dataset.modern
  };

  function applyTheme(themeName, persist) {
    if (!themes[themeName]) {
      return;
    }

    themeLink.setAttribute("href", themes[themeName]);
    document.documentElement.setAttribute("data-theme", themeName);
    document.dispatchEvent(new CustomEvent("fintrack:theme-change", { detail: { theme: themeName } }));

    if (persist) {
      localStorage.setItem("fintrack-theme", themeName);
    }
  }

  var storedTheme = localStorage.getItem("fintrack-theme");
  var initialTheme = themes[storedTheme] ? storedTheme : "wireframe";

  applyTheme(initialTheme, false);

  if (selector) {
    selector.value = initialTheme;
    selector.addEventListener("change", function (event) {
      applyTheme(event.target.value, true);
    });
  }
})();
