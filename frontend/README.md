# Team 68 - App de Educacion Financiera

Este repositorio contiene el frontend estatico y navegable de Team 68, una aplicacion de educacion financiera pensada para ayudar a los usuarios a entender y mejorar sus habitos de consumo a partir del registro de ingresos, gastos y analisis inteligente de su informacion financiera.

La propuesta funcional combina visualizacion clara, clasificacion de movimientos y recomendaciones practicas para apoyar decisiones de presupuesto, prioridades de gasto y estrategias de ahorro.

## Versiones

Version actual: 0.3

Version 0.1: Prototipo inicial
Version 0.2: Grafica de ingresos y gastos
Version 0.3: Grafica de salud financiera

## Descripcion del proyecto

Team 68 busca ofrecer una experiencia simple, intuitiva y confiable para organizar finanzas personales, detectar patrones de consumo y recibir orientacion accionable basada en datos reales.

En este workspace se representa esa propuesta mediante un wireframe frontend con pantallas de bienvenida, resumen, ingresos, gastos, historial, salud financiera y login, listo para validar contenido, navegacion y enfoque visual del producto.

## Objetivo

- Organizar ingresos y gastos personales en una interfaz clara y accesible.
- Detectar patrones de consumo y comportamientos de riesgo financiero.
- Presentar recomendaciones personalizadas para mejorar la salud financiera del usuario.

## Caracteristicas principales

- Registro de ingresos y gastos con categorizacion flexible.
- Visualizacion dinamica de movimientos y distribucion de gastos.
- Analisis del comportamiento financiero y clasificacion del perfil del usuario.
- Recomendaciones de presupuesto mensual, alertas de riesgo y sugerencias de ahorro.
- Navegacion entre pantallas clave del flujo del producto.
- Cambio de tema visual con persistencia mediante localStorage.

## Como funciona la solucion

1. El usuario registra sus ingresos, gastos y datos basicos de perfil financiero.
2. El backend valida la informacion y procesa el historial transaccional.
3. El motor de IA analiza patrones de consumo y clasifica el perfil financiero.
4. El sistema devuelve recomendaciones y alertas en un formato interpretable por el frontend.
5. La interfaz muestra resumenes, tendencias y mensajes accionables para la toma de decisiones.

## Alcance actual del repositorio

Este repositorio implementa la capa frontend del MVP como maqueta funcional en HTML, CSS y JavaScript. La arquitectura objetivo del producto tambien contempla un backend en Spring Boot, integracion con un modelo ONNX y despliegue en OCI, pero esos componentes no forman parte de este workspace.

## Requisitos minimos del MVP

- Registro y visualizacion de movimientos financieros.
- Validacion de entradas para evitar datos inconsistentes.
- Clasificacion funcional de transacciones por categoria.
- Analisis del perfil financiero del usuario.
- Generacion de recomendaciones accionables.
- Visualizacion clara de resultados y metricas relevantes.

## Arquitectura tecnologica objetivo

### Frontend

- HTML5, CSS3 y JavaScript moderno.
- Bootstrap 5 para estructura responsive.
- Chart.js para visualizacion de tendencias y categorias.
- DataTables, SweetAlert2, Intro.js e Ionicons para soporte de interaccion y experiencia.

### Backend

- Java 17+ con Spring Boot 3.x.
- API REST documentada con Swagger / OpenAPI.
- Endpoints esperados para analisis financiero y clasificacion de transacciones.
- Validacion de datos y manejo centralizado de errores.

### IA y ciencia de datos

- Entrenamiento del modelo en Python.
- Exportacion del modelo a ONNX para ejecucion integrada en backend.
- Analisis descriptivo y predictivo sobre historicos y variables de perfil.

### Infraestructura objetivo

- OCI Compute para despliegue del frontend y backend.
- OCI Autonomous Database para persistencia de datos.
- OCI Object Storage para resguardo de artefactos y modelos.

## Valor para el usuario

- Mayor autonomia financiera mediante informacion clara y util.
- Recomendaciones inmediatas basadas en patrones detectados.
- Una base escalable para evolucionar hacia una plataforma de educacion financiera asistida por IA.

## Estructura del proyecto

- index.html
  - Redirige automaticamente a la vista principal dentro de public/.
- public/
  - pages/
    - welcome.html: portada con propuesta de valor del producto.
    - login.html: pantalla de inicio de sesion.
    - summary.html: resumen mensual y ultimos movimientos.
    - income.html: formulario de carga de ingresos.
    - expense.html: formulario de carga de gastos.
    - history.html: filtros, tabla historica y grafica de categorias.
    - salud-financiera.html: indicadores de salud financiera, sugerencias y medallas obtenidas.
    - logout.html: salida y redireccion.
  - assets/css/
    - wireframe.css: estilo tipo boceto.
    - modern.css: estilo visual moderno.
    - y2k.css: variante visual retro.
    - hollow.css: variante visual alternativa.
  - assets/js/
    - theme-switcher.js: cambio de tema y persistencia.
    - forms-local.js: comportamiento local de formularios.
    - movements-local.js: datos y movimientos de ejemplo.
    - page-help.js: ayuda contextual.
  - vendor/
    - bootstrap: estilos y componentes.
    - datatables: tabla interactiva.
    - sweetalert2: modales y alertas.
    - ionicons: iconografia.
    - chartjs: renderizado de graficas.
    - introjs: guias paso a paso.

## Tecnologias usadas en este workspace

- HTML5
- CSS3
- JavaScript vanilla
- Bootstrap 5
- DataTables
- SweetAlert2
- Chart.js
- Intro.js
- Ionicons
