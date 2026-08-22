# Team 68 - App de Educación Financiera

Este repositorio contiene el frontend estático y navegable de Team 68, una aplicación de educación financiera pensada para ayudar a los usuarios a entender y mejorar sus hábitos de consumo a partir del registro de ingresos, gastos y análisis inteligente de su información financiera.

La propuesta funcional combina visualización clara, clasificación de movimientos y recomendaciones prácticas para apoyar decisiones de presupuesto, prioridades de gasto y estrategias de ahorro.

## Versiones

Versión actual: 1.0

Versión 0.1: Prototipo inicial
Versión 0.2: Gráfica de gastos
Versión 0.3: Gráfica de perfil financiero
Versión 0.4: Ajustes de la simulación
Versión 0.5: Método de pago en gastos
Versión 0.6: Fixes y optimizaciones
Versión 0.7: Diseno de interfaz Rendi
Versión 0.8: Integracion con API remota
Versión 0.9: Fallback local en metricas
Versión 1.0: Edición y eliminación de movimientos
Versión 1.1: Fixes en fallback de perfil

## Descripción del proyecto

Team 68 busca ofrecer una experiencia simple, intuitiva y confiable para organizar finanzas personales, detectar patrones de consumo y recibir orientación accionable basada en datos reales.

En este workspace se representa esa propuesta mediante un prototipo frontend con pantallas de bienvenida, resumen, ingresos, gastos, historial, perfil y login, listo para validar contenido, navegación y enfoque visual del producto.

## Objetivo

- Organizar ingresos y gastos personales en una interfaz clara y accesible.
- Detectar patrones de consumo y comportamientos de riesgo financiero.
- Presentar recomendaciones personalizadas para mejorar la salud financiera del usuario.

## Características principales

- Registro de ingresos y gastos con categorización flexible.
- Visualización dinámica de movimientos y distribución de gastos.
- Análisis del comportamiento financiero y clasificación del perfil del usuario.
- Recomendaciones personalizadas basadas en datos reales.
- Navegacion entre pantallas clave del flujo del producto.
- Cambio de tema visual con persistencia mediante localStorage.

## Cómo funciona la solución

1. El usuario registra sus ingresos, gastos y datos básicos de perfil financiero.
2. El backend valida la información y procesa el historial transaccional.
3. El motor de IA analiza patrones de consumo y clasifica el perfil financiero.
4. El sistema devuelve recomendaciones y alertas en un formato interpretable por el frontend.
5. La interfaz muestra resúmenes, tendencias y mensajes accionables para la toma de decisiones.

## Alcance actual del repositorio

Este repositorio implementa la capa frontend del MVP como maqueta funcional en HTML, CSS y JavaScript. La arquitectura objetivo del producto tambien contempla un backend en Spring Boot, integracion con un modelo ONNX y despliegue en OCI, pero esos componentes no forman parte de este workspace.

## Requisitos mínimos del MVP

- Registro y visualización de movimientos financieros.
- Validación de entradas para evitar datos inconsistentes.
- Clasificacion funcional de transacciones por categoría.
- Analisis del perfil financiero del usuario.
- Generación de recomendaciones accionables.
- Visualizacion clara de resultados y métricas relevantes.

## Arquitectura tecnológica objetivo

### Frontend

- HTML5, CSS3 y JavaScript moderno.
- Bootstrap 5 para estructura responsive.
- Chart.js para visualizacion de tendencias y categorías.
- SweetAlert2, Intro.js y Font Awesome para soporte de interacción y experiencia.

### Backend

- Java 17+ con Spring Boot 3.x.
- API REST documentada con Swagger / OpenAPI.
- Endpoints esperados para análisis financiero y clasificacion de transacciones.
- Validación de datos y manejo centralizado de errores.

### IA y ciencia de datos

- Entrenamiento del modelo en Python.
- Exportación del modelo a ONNX para ejecución integrada en backend.
- Análisis descriptivo y predictivo sobre historicos y variables de perfil.

### Infraestructura objetivo

- OCI Compute para despliegue del frontend y backend.
- OCI Autonomous Database para persistencia de datos.
- OCI Object Storage para resguardo de artefactos y modelos.

## Valor para el usuario

- Mayor autonomía financiera mediante información clara  y útil.
- Recomendaciones inmediatas basadas en patrones detectados.
- Una base escalable para evolucionar hacia una plataforma de educación financiera asistida por IA.

## Estructura del proyecto

- index.html
  - Redirige automaticamente a la vista principal dentro de public/.
- public/
  - pages/
    - welcome.html: portada con propuesta de valor del producto.
    - login.html: pantalla de inicio de sesión.
    - summary.html: resumen mensual y últimos movimientos.
    - income.html: formulario de carga de ingresos.
    - expense.html: formulario de carga de gastos.
    - history.html: filtros, tabla histórica y grafica de categorías.
    - perfil.html: indicadores de salud financiera, sugerencias y medallas obtenidas.
    - logout.html: salida y redirección.
  - assets/css/
    - wireframe.css: estilo tipo boceto.
    - y2k.css: variante visual retro.
    - hollow.css: variante visual alternativa.
    - rendi.css: estilo y diseño de rendi.
  - assets/js/
    - theme-switcher.js: cambio de tema y persistencia.
    - movements.js: datos y movimientos de ejemplo.
    - page-help.js: ayuda contextual.
  - vendor/
    - bootstrap: estilos y componentes.
    - sweetalert2: modales y alertas.
    - fontawesome: iconografía.
    - chartjs: renderizado de gráficas.
    - introjs: guías paso a paso.
