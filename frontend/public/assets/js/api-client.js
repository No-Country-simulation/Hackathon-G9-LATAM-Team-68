(function () {
  var API_BASE_URL = "https://hackathon-g9-latam-team-68.onrender.com";
  var SESSION_KEY = "team68-session";
  var LOCAL_SESSION_ID_KEY = "team68-local-user-id";

  function safeParseJSON(raw) {
    try {
      return JSON.parse(raw);
    } catch (error) {
      return null;
    }
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

    return parsed;
  }

  function saveSession(session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }

  function clearSession() {
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem("team68-movimientos-cache");
    localStorage.removeItem("team68-financial-profile");
  }

  function isAuthenticated() {
    var session = getSession();
    return !!(session && session.id);
  }

  function getOrCreateLocalUserId() {
    var existing = localStorage.getItem(LOCAL_SESSION_ID_KEY);
    if (existing) {
      return existing;
    }

    var nextId;
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      nextId = window.crypto.randomUUID();
    } else {
      nextId = "00000000-0000-0000-0000-000000000001";
    }

    localStorage.setItem(LOCAL_SESSION_ID_KEY, nextId);
    return nextId;
  }

  async function request(path, options) {
    var config = options || {};
    var headers = Object.assign({}, config.headers || {});
    var session = getSession();

    if (config.body && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }

    if (config.auth !== false && session && session.token) {
      headers.Authorization = "Bearer " + session.token;
    }

    var response = await fetch(API_BASE_URL + path, {
      method: config.method || "GET",
      headers: headers,
      body: config.body
    });

    var text = await response.text();
    var payload = text ? safeParseJSON(text) || text : null;

    if (!response.ok) {
      throw new Error(normalizeErrorMessage(response, payload));
    }

    return payload;
  }

  async function login(username, password) {
    var cleanUser = String(username || "").trim();
    var cleanPassword = String(password || "");
    if (!cleanUser || !cleanPassword) {
      throw new Error("Debes ingresar usuario y contrasena.");
    }

    var session = {
      id: getOrCreateLocalUserId(),
      username: cleanUser,
      nombre: cleanUser,
      token: ""
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
    return request("/api/ingresos/usuario/" + encodeURIComponent(usuarioId));
  }

  function crearIngreso(usuarioId, payload) {
    return request("/api/ingresos/usuario/" + encodeURIComponent(usuarioId), {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  function getMovimientosUsuario(usuarioId) {
    return request("/api/movimientos/usuario/" + encodeURIComponent(usuarioId));
  }

  function crearTransaccion(usuarioId, payload) {
    return request("/api/movimientos/usuario/" + encodeURIComponent(usuarioId), {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  function realizarAnalisis(payload) {
    return request("/api/analisis", {
      method: "POST",
      body: JSON.stringify(payload)
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
