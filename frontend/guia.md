# Guia de integracion API

## 1. Alcance actual
Esta version usa el backend para todo el flujo de datos de negocio:
- Registros (ingresos y gastos): API.
- Analisis financiero: API.
- Perfil financiero: API.

El login se mantiene local para habilitar la sesion de UI sin llamar al endpoint de autenticacion.

## 2. Endpoints usados
Base URL:
- `https://hackathon-g9-latam-team-68.onrender.com`

Operaciones:
- `GET /api/ingresos/usuario/{usuarioId}`
- `POST /api/ingresos/usuario/{usuarioId}`
- `GET /api/movimientos/usuario/{usuarioId}`
- `POST /api/movimientos/usuario/{usuarioId}`
- `POST /api/analisis`

## 3. Flujo de sesion
- `public/assets/js/login-local.js` usa `team68Api.login(...)`.
- `public/assets/js/api-client.js` implementa login local:
  - valida usuario/contrasena no vacios,
  - crea o reutiliza un `usuarioId` local UUID,
  - guarda sesion en `localStorage` (`team68-session`).
- `requireAuth()` protege vistas internas y redirige a login si no hay sesion.

## 4. Flujo de registros
Archivo principal:
- `public/assets/js/movements-local.js`

Comportamiento:
1. Al cargar vistas protegidas, ejecuta sincronizacion API (`syncFromApi`).
2. Obtiene ingresos y movimientos del usuario por `usuarioId`.
3. Renderiza tablas/totales con esos datos.
4. Al crear registro (`addMovement`), envia POST al backend y actualiza vista con respuesta API.

Nota:
- No hay datos semilla.
- No hay fallback local de registros cuando falla API.

## 5. Flujo de analisis y perfil
Analisis:
- Se arma payload desde registros actuales en memoria (origen API).
- Se envia a `POST /api/analisis`.

Perfil:
- `perfil.html` lee el resultado desde `localStorage` (`team68-financial-profile`) que se llena solo con respuesta API.
- Si el analisis no esta disponible, muestra estado "sin datos del api".
- Se refresca al recibir eventos:
  - `team68:movements-updated`
  - `team68:profile-updated`

## 6. Formularios
Archivo:
- `public/assets/js/forms-local.js`

Reglas actuales:
- Ingreso: envia fecha, descripcion y monto.
- Gasto: envia fecha, descripcion, monto, forma de pago y tasa si aplica.
- Categoria de gasto no se envia desde formulario; el backend la determina.

## 7. Mensajeria y estados
- Toasts de sincronizacion en `movements-local.js`:
  - cargando,
  - exito,
  - error.
- Cuando la API falla en sincronizacion:
  - se vacian registros en vista,
  - se limpia perfil API en almacenamiento,
  - se informa el error.

## 8. Archivos clave
- `public/assets/js/api-client.js`: cliente API + sesion local.
- `public/assets/js/login-local.js`: login UI.
- `public/assets/js/logout-local.js`: cierre de sesion.
- `public/assets/js/movements-local.js`: sincronizacion registros + analisis.
- `public/assets/js/forms-local.js`: captura y envio de formularios.
- `public/pages/perfil.html`: visualizacion del perfil proveniente de API.
