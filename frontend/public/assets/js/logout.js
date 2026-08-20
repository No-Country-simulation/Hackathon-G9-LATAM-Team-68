(function () {
  if (window.team68Api && typeof window.team68Api.logout === "function") {
    window.team68Api.logout();
  }

  window.location.replace("login.html");
})();
