# Team 68 - App de Educación Financiera

Aplicación web de educación y gestión financiera personal desarrollada por **Team 68**.

El proyecto busca ayudar al usuario a comprender su comportamiento financiero mediante el registro de ingresos y gastos, visualización de movimientos, análisis de salud financiera y generación de recomendaciones orientadas a mejorar sus hábitos de consumo, ahorro y administración del dinero.

El frontend implementa un flujo navegable de aplicación web con autenticación, dashboard financiero, registro de ingresos y gastos, historial de movimientos, análisis de salud financiera y recomendaciones personalizadas.

## Versiones

**Versión actual: 1.1**

- **Versión 0.1:** Prototipo inicial.
- **Versión 0.2:** Incorporación de gráfica de gastos.
- **Versión 0.3:** Incorporación de gráfica de perfil financiero.
- **Versión 0.4:** Ajustes de la simulación.
- **Versión 0.5:** Incorporación del método de pago en gastos.
- **Versión 0.6:** Correcciones y optimizaciones.
- **Versión 0.7:** Rediseño de interfaz Rendi.
- **Versión 0.8:** Integración con API remota.
- **Versión 0.9:** Implementación de fallback local para métricas.
- **Versión 1.0:** Edición y eliminación de movimientos.
- **Versión 1.1:** Correcciones y mejoras en el fallback del perfil financiero.

## Descripción del proyecto

Team 68 propone una herramienta de apoyo para la educación financiera personal que transforma los movimientos económicos registrados por el usuario en información fácil de interpretar.

La aplicación permite registrar ingresos y gastos, consultar el historial financiero, visualizar la distribución de los gastos y obtener un análisis de la salud financiera.

El sistema combina dos mecanismos de procesamiento:

1. **Integración con API remota**, utilizada cuando el backend se encuentra disponible.
2. **Procesamiento local de respaldo**, que permite mantener determinadas funcionalidades del frontend cuando la API no está disponible.

De esta forma, el prototipo puede continuar mostrando información y métricas esenciales incluso ante problemas temporales de conectividad con los servicios externos.

## Objetivo

- Facilitar el registro y control de ingresos y gastos personales.
- Ayudar al usuario a identificar sus principales categorías de consumo.
- Mostrar indicadores comprensibles sobre su comportamiento financiero.
- Clasificar el estado o perfil financiero del usuario.
- Generar sugerencias prácticas para mejorar sus hábitos financieros.
- Presentar la información mediante gráficos, indicadores y componentes visuales fáciles de interpretar.
- Proporcionar una experiencia de usuario sencilla y accesible.

## Flujo principal de la aplicación

El flujo general del frontend se organiza de la siguiente manera:

**Bienvenida → Inicio de sesión → Resumen financiero → Registro de movimientos → Historial → Salud financiera → Recomendaciones**

### 1. Bienvenida

La pantalla inicial presenta la propuesta de valor de la aplicación y dirige al usuario hacia el acceso al sistema.

### 2. Inicio de sesión

El usuario puede acceder mediante la pantalla de autenticación.

El frontend dispone de lógica de conexión remota y mecanismos locales de respaldo para el flujo de autenticación.

### 3. Resumen financiero

El dashboard presenta una visión general de la situación financiera del usuario, incluyendo información relacionada con ingresos, gastos, movimientos recientes y métricas financieras.

### 4. Registro de ingresos

Permite incorporar nuevos ingresos indicando la información necesaria para clasificar y registrar el movimiento.

### 5. Registro de gastos

Permite registrar gastos y asociarlos con categorías y método de pago para obtener posteriormente una mejor lectura del comportamiento de consumo.

### 6. Historial financiero

Presenta los movimientos registrados y permite consultar la información histórica.

El sistema contempla operaciones de:

- Consulta de movimientos.
- Filtrado de información.
- Visualización de categorías.
- Edición de movimientos.
- Eliminación de movimientos.
- Visualización gráfica de la distribución de gastos.

### 7. Salud financiera

La aplicación incorpora una sección específica para analizar el comportamiento financiero.

Esta sección presenta indicadores y resultados destinados a facilitar la interpretación de la situación económica del usuario.

El análisis puede complementarse con recomendaciones y elementos de gamificación, como sugerencias y medallas.

### 8. Recomendaciones

A partir de las métricas obtenidas, la interfaz presenta recomendaciones orientadas a acciones concretas, como control del presupuesto, ahorro y mejora de los hábitos de consumo.

## Características principales

- Registro de ingresos.
- Registro de gastos.
- Categorización de movimientos.
- Registro del método de pago.
- Historial financiero.
- Edición de movimientos.
- Eliminación de movimientos.
- Filtros para consulta de movimientos.
- Gráficas de distribución de gastos.
- Indicadores de salud financiera.
- Clasificación del perfil financiero.
- Recomendaciones personalizadas.
- Sistema de medallas y elementos de gamificación.
- Autenticación.
- Integración con API remota.
- Fallback local para funcionalidades críticas.
- Validación de formularios.
- Mensajes y alertas de interacción.
- Ayuda contextual.
- Guías de navegación.
- Diseño responsive.
- Cambio de tema visual con persistencia mediante `localStorage`.

## Integración con API y fallback local

El frontend está preparado para trabajar con servicios remotos mediante una capa específica de comunicación con la API.

La implementación actual incluye archivos separados para las operaciones:

- `api-client.js`: comunicación con los servicios de API.
- `login.js`: autenticación.
- `forms.js`: procesamiento de formularios.
- `movements.js`: gestión de movimientos.
- `logout.js`: cierre de sesión.

Esta separación permite desacoplar la interfaz de la disponibilidad del backend y facilita las pruebas del MVP.

## Arquitectura funcional

```
                    ┌─────────────────────┐
                    │      Usuario        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Frontend        │
                    │ HTML + CSS + JS     │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │    API remota    │      │  Fallback local  │
        │   Backend REST   │      │   del frontend   │
        └────────┬─────────┘      └────────┬─────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                   ┌──────────────────────┐
                   │ Métricas financieras │
                   │ Perfil / sugerencias │
                   └──────────────────────┘
```

## Alcance actual del repositorio

Este repositorio contiene principalmente la capa **frontend** del MVP.

La aplicación está construida como un sitio web estático utilizando HTML, CSS y JavaScript, pero incorpora lógica suficiente para consumir servicios financieros reales mediante API.

El repositorio permite validar:

- Flujo de navegación.
- Experiencia de usuario.
- Registro de movimientos.
- Visualización financiera.
- Integración con servicios REST.
- Comportamiento ante indisponibilidad de la API.
- Presentación de métricas.
- Perfil y salud financiera.
- Recomendaciones.
- Diseño responsive.

La arquitectura completa del producto puede incorporar posteriormente los servicios backend, persistencia, modelos de IA y componentes de infraestructura.

## Tecnologías

### Frontend

- HTML5.
- CSS3.
- JavaScript moderno.
- Bootstrap 5.
- Chart.js.
- SweetAlert2.
- Intro.js.
- Font Awesome.
- `localStorage` para persistencia de determinadas preferencias y datos locales.

### Integración

- API REST mediante JavaScript.
- Comunicación mediante `fetch`.
- Separación entre lógica remota y fallback local.
- Procesamiento de respuestas de servicios financieros.
- Manejo de errores y escenarios de indisponibilidad del backend.

## IA y análisis financiero

La solución está diseñada para evolucionar hacia un sistema de análisis financiero asistido por IA.

El flujo previsto contempla:

1. Recopilación de movimientos financieros.
2. Procesamiento de variables financieras.
3. Identificación de patrones de consumo.
4. Clasificación del perfil financiero.
5. Generación de métricas.
6. Generación de recomendaciones.
7. Presentación de los resultados dentro del frontend.

La arquitectura objetivo contempla la utilización de un modelo desarrollado en Python y eventualmente exportado a ONNX para su integración con el backend.

## Infraestructura objetivo

La arquitectura propuesta para una versión productiva contempla:

- **OCI Compute** para servicios de aplicación.
- **OCI Autonomous Database** para persistencia.
- **OCI Object Storage** para almacenamiento de artefactos y modelos.
- Backend basado en Spring Boot.
- API REST documentada mediante Swagger / OpenAPI.

Estos componentes corresponden a la arquitectura objetivo y no representan necesariamente dependencias directas del frontend contenido en este repositorio.

## Estructura del proyecto

```
frontend/
│
├── index.html
│
├── README.md
├── VERSION
├── guia.md
│
└── public/
    │
    ├── pages/
    │   ├── welcome.html
    │   ├── login.html
    │   ├── summary.html
    │   ├── income.html
    │   ├── expense.html
    │   ├── history.html
    │   ├── perfil.html
    │   ├── salud-financiera.html
    │   └── logout.html
    │
    ├── assets/
    │   │
    │   ├── css/
    │   │   ├── hollow.css
    │   │   ├── modern.css
    │   │   ├── rendi.css
    │   │   ├── wireframe.css
    │   │   └── y2k.css
    │   │
    │   ├── fonts/
    │   │
    │   ├── images/
    │   │
    │   └── js/
    │       ├── api-client.js
    │       ├── forms.js
    │       ├── login.js
    │       ├── logout.js
    │       ├── movements.js
    │       ├── page-help.js
    │       └── theme-switcher.js
    │
    └── vendor/
        ├── bootstrap/
        ├── sweetalert2/
        ├── fontawesome/
        ├── chartjs/
        └── introjs/
```

## Descripción de las páginas

| Página | Función |
|---|---|
| `welcome.html` | Presentación de la aplicación y propuesta de valor. |
| `login.html` | Inicio de sesión del usuario. |
| `summary.html` | Dashboard y resumen de la situación financiera. |
| `income.html` | Registro de ingresos. |
| `expense.html` | Registro de gastos y método de pago. |
| `history.html` | Consulta, filtrado, edición y eliminación de movimientos. |
| `perfil.html` | Perfil financiero, indicadores, sugerencias y elementos de gamificación. |
| `salud-financiera.html` | Análisis específico de la salud financiera. |
| `logout.html` | Cierre de sesión y redirección. |

## Sistema visual

El frontend incorpora diferentes hojas de estilo que permiten evolucionar y probar distintas propuestas visuales:

- `rendi.css`: identidad visual principal de Rendi.
- `modern.css`: propuesta visual moderna.
- `wireframe.css`: estilo de prototipo/wireframe.
- `y2k.css`: propuesta estética Y2K.
- `hollow.css`: variante visual alternativa.

Esta estructura permite mantener separada la presentación visual de la lógica funcional.

## Experiencia de usuario

El proyecto incorpora elementos orientados a mejorar la UX:

- Diseño responsive.
- Navegación entre módulos.
- Alertas visuales.
- Confirmaciones para operaciones sensibles.
- Ayuda contextual.
- Guías paso a paso.
- Iconografía mediante Font Awesome.
- Gráficas para facilitar la interpretación de datos.
- Cambio de tema.
- Persistencia de preferencias mediante `localStorage`.

## Requisitos mínimos del MVP

El MVP debe permitir:

- Registrar ingresos.
- Registrar gastos.
- Clasificar movimientos.
- Registrar método de pago.
- Consultar movimientos históricos.
- Editar movimientos.
- Eliminar movimientos.
- Visualizar métricas financieras.
- Analizar el perfil financiero.
- Mostrar indicadores de salud financiera.
- Generar recomendaciones.
- Mantener una experiencia funcional cuando la API remota no esté disponible mediante mecanismos de fallback.

## Valor para el usuario

La aplicación busca convertir datos financieros cotidianos en información útil para la toma de decisiones.

El usuario puede pasar de simplemente registrar movimientos a comprender:

- cuánto dinero recibe;
- cuánto gasta;
- en qué categorías concentra sus gastos;
- cómo evoluciona su comportamiento financiero;
- cuál es su situación financiera;
- qué aspectos puede mejorar;
- qué acciones puede tomar para fortalecer sus hábitos de ahorro y consumo.

## Demo

El frontend puede ejecutarse como sitio estático y también desplegarse mediante servicios como GitHub Pages.

El proyecto está disponible en el repositorio oficial:

`https://github.com/No-Country-simulation/Hackathon-G9-LATAM-Team-68`

La carpeta principal del frontend se encuentra en:

`frontend/`

## Equipo

**Team 68 — Hackathon G9 LATAM**

Proyecto orientado a educación financiera, análisis de comportamiento financiero y generación de recomendaciones accionables mediante tecnología web e inteligencia artificial.
