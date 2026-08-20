# Team68 Wireframe - App de Ingresos y Gastos

Versión actual: 0.1

Proyecto frontend estático que presenta el wireframe de una aplicación para registrar ingresos y gastos, revisar historial y visualizar un resumen mensual.

## Objetivo

Proveer una maqueta navegable para validar flujo, contenido y estilos visuales antes de implementar lógica de negocio y persistencia de datos.

## Características

- Navegación entre pantallas de bienvenida, login, resumen, ingresos, gastos, historial y logout.
- Cuatro estilos visuales intercambiables:
  - Default (Bootstrap)
  - Wireframe
  - Modern
  - Y2K
- Persistencia del estilo seleccionado en el navegador mediante localStorage.
- Gráfica de gastos por categoría en la vista de historial con Chart.js.
- Interfaz responsive basada en Bootstrap.

## Estructura del proyecto

- index.html
  - Redirige automáticamente a la vista de resumen dentro de public/.
- public/
  - pages/
    - welcome.html: portada del wireframe.
    - login.html: pantalla de inicio de sesión (maqueta).
    - summary.html: resumen mensual y últimos movimientos.
    - income.html: formulario de carga de ingresos.
    - expense.html: formulario de carga de gastos.
    - history.html: filtros, tabla histórica y gráfica de categorías.
    - logout.html: redirección a login.
  - assets/css/
    - wireframe.css: estilo tipo boceto.
    - modern.css: estilo visual moderno.
    - hollow.css: estilo inspirado en Hollow Knight.
  - assets/js/
    - theme-switcher.js: cambio de tema y persistencia.
  - vendor/
    - bootstrap: estilos y componentes.
    - datatables: tabla interactiva.
    - sweetalert2: modales y alertas.
    - ionicons: iconografía.
    - chartjs: renderizado de gráfica.
    - introjs: guías paso a paso.

## Tecnologías

- HTML5
- CSS3
- JavaScript (vanilla)
- Bootstrap 5
- DataTables
- SweetAlert2
- Chart.js
- Intro.js
- Ionicons
