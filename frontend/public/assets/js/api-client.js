(function () {
  var API_BASE_URL = "https://hackathon-g9-latam-team-68.onrender.com";
  var SESSION_KEY = "team68-session";

  function safeParseJSON(raw) {
    try {
      return JSON.parse(raw);
    } catch (error) {
      return null;
    }
  }

  function isValidUuid(value) {
    return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(String(value || ""));
  }

  function normalizeErrorMessage(response, payload) {
    if (!payload) {
      return "No fue posible completar la solicitud.";
    }

    if (typeof payload === "string") {
      return payload;
    }

    if (payload.message) {
      return String(payload.message);
    }

    if (payload.error) {
      return String(payload.error);
    }

    if (payload.detalle) {
      return String(payload.detalle);
    }

    if (response && response.status === 401) {
      return "Tu sesion ha expirado. Inicia sesion nuevamente.";
    }

    return "No fue posible completar la solicitud.";
  }

  function getSession() {
    var raw = localStorage.getItem(SESSION_KEY);
    if (!raw) {
      return null;
    }

    var parsed = safeParseJSON(raw);
    if (!parsed || typeof parsed !== "object") {
      return null;
    }

    if (!isValidUuid(parsed.id)) {
      return null;
    }

    return parsed;
  }

  function saveSession(session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }

  function clearSession() {
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem("team68-financial-profile");
  }

  function isAuthenticated() {
    var session = getSession();
    return !!(session && session.id);
  }

  async function request(path, options) {
    var config = options || {};
    var headers = Object.assign({}, config.headers || {});
    var session = getSession();
    var method = config.method || "GET";
    var endpoint = path;
    var operation = config.operation || "api";

    if (config.body && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }

    if (config.auth !== false && session && session.token) {
      headers.Authorization = "Bearer " + session.token;
    }

    try {
      var response = await fetch(API_BASE_URL + path, {
        method: method,
        headers: headers,
        body: config.body
      });

      var text = await response.text();
      var payload = text ? safeParseJSON(text) || text : null;

      if (!response.ok) {
        var httpErrorMessage = normalizeErrorMessage(response, payload);
        throw new Error(httpErrorMessage);
      }

      return payload;
    } catch (error) {
      throw error;
    }
  }

  async function login(username, password) {
    var cleanUser = String(username || "").trim();
    var cleanPassword = String(password || "");
    if (!cleanUser || !cleanPassword) {
      throw new Error("Debes ingresar usuario y contrasena.");
    }

    var authResponse = await request("/api/auth/login", {
      method: "POST",
      auth: false,
      body: JSON.stringify({
        username: cleanUser,
        password: cleanPassword
      }),
      operation: "iniciar sesion"
    });

    if (!authResponse || !authResponse.id) {
      throw new Error("La API no devolvio un identificador de usuario valido.");
    }

    var session = {
      id: String(authResponse.id),
      username: String(authResponse.username || cleanUser),
      nombre: String(authResponse.nombre || authResponse.username || cleanUser),
      token: String(authResponse.token || "")
    };

    saveSession(session);
    return session;
  }

  function logout() {
    clearSession();
  }

  function getUsuarioId() {
    var session = getSession();
    return session ? session.id : null;
  }

  function getUsuarioNombre() {
    var session = getSession();
    return session ? (session.nombre || session.username || "Usuario") : "Usuario";
  }

  function requireAuth() {
    if (isAuthenticated()) {
      return true;
    }

    window.location.replace("login.html");
    return false;
  }

  function getIngresosUsuario(usuarioId) {
    return request("/api/ingresos/usuario/" + encodeURIComponent(usuarioId), {
      operation: "listar ingresos"
    });
  }

  function crearIngreso(usuarioId, payload) {
    return request("/api/ingresos/usuario/" + encodeURIComponent(usuarioId), {
      method: "POST",
      body: JSON.stringify(payload),
      operation: "registrar ingreso"
    });
  }

  function getMovimientosUsuario(usuarioId) {
    return request("/api/movimientos/usuario/" + encodeURIComponent(usuarioId), {
      operation: "listar movimientos"
    });
  }

  function crearTransaccion(usuarioId, payload) {
    return request("/api/movimientos/usuario/" + encodeURIComponent(usuarioId), {
      method: "POST",
      body: JSON.stringify(payload),
      operation: "registrar movimiento"
    });
  }

  function realizarAnalisis(payload) {
    return request("/api/analisis/analizar", {
      method: "POST",
      body: JSON.stringify(payload),
      operation: "analisis financiero"
    });
  }

  window.team68Api = {
    login: login,
    logout: logout,
    getSession: getSession,
    isAuthenticated: isAuthenticated,
    requireAuth: requireAuth,
    getUsuarioId: getUsuarioId,
    getUsuarioNombre: getUsuarioNombre,
    getIngresosUsuario: getIngresosUsuario,
    crearIngreso: crearIngreso,
    getMovimientosUsuario: getMovimientosUsuario,
    crearTransaccion: crearTransaccion,
    realizarAnalisis: realizarAnalisis
  };
})();
