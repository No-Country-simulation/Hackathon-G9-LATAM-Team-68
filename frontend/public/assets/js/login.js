(function () {
  function showMessage(icon, title, text) {
    if (window.Swal) {
      window.Swal.fire({
        toast: true,
        position: "bottom-end",
        icon: icon,
        title: title,
        text: text,
        timer: icon === "error" ? 3200 : 1800,
        showConfirmButton: false,
        timerProgressBar: true
      });
      return;
    }

    alert(title + ": " + text);
  }

  async function onSubmit(event) {
    event.preventDefault();

    if (!window.team68Api) {
      showMessage("error", "Error", "No se encontro el cliente API.");
      return;
    }

    var userInput = document.getElementById("user");
    var passwordInput = document.getElementById("password");
    var submitButton = document.querySelector("#loginForm button[type='submit']");
    var username = userInput ? userInput.value.trim() : "";
    var password = passwordInput ? passwordInput.value : "";

    if (!username || !password) {
      showMessage("warning", "Datos incompletos", "Ingresa usuario y contrasena.");
      return;
    }

    if (submitButton) {
      submitButton.disabled = true;
    }

    try {
      await window.team68Api.login(username, password);
      showMessage("success", "Sesion iniciada", "Redirigiendo al resumen...");
      window.setTimeout(function () {
        window.location.replace("summary.html");
      }, 500);
    } catch (error) {
      showMessage("error", "No se pudo iniciar sesion", error.message || "Credenciales invalidas");
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
      }
    }
  }

  function init() {
    if (!window.team68Api) {
      return;
    }

    if (window.team68Api.isAuthenticated()) {
      window.location.replace("summary.html");
      return;
    }

    var form = document.getElementById("loginForm");
    if (!form) {
      return;
    }

    form.addEventListener("submit", onSubmit);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
