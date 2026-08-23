# Team 68 - FinanceAI: App de Educación Financiera

## Descripción del Proyecto
Team 68 es una aplicación de educación financiera enfocada en ayudar a los usuarios a entender y mejorar sus hábitos de consumo mediante el análisis inteligente de sus datos transaccionales y su perfil financiero.

La plataforma permite registrar ingresos y gastos, analizar el comportamiento financiero con Inteligencia Artificial y generar recomendaciones prácticas de presupuesto, prioridades de gasto y estrategias de ahorro — todo esto acompañado de un sistema de gamificación que premia los buenos hábitos financieros.

## Objetivo
Ofrecer una herramienta simple, intuitiva y confiable para:
- Organizar ingresos y gastos personales.
- Detectar patrones de consumo y comportamientos de riesgo.
- Recibir recomendaciones personalizadas basadas en datos reales para una mejor salud financiera.
- Motivar la mejora de hábitos financieros mediante un sistema de logros.

## Características Principales
- **Registro de Ingresos y Gastos:** Control detallado de movimientos financieros.
- **Clasificación Automática de Transacciones:** Un servicio de inteligencia artificial clasifica cada transacción según su tipo (Consumo, Pago de deuda, Ahorro e inversión) y categoría (Vivienda, Alimentación, Transporte, Salud, Educación, Entretenimiento, Suscripciones, Compras personales, Viajes, Otros).
- **Análisis del Perfil Financiero:** Evaluación en 4 dimensiones (Balance financiero, Capacidad de ahorro, Endeudamiento, Comportamiento de consumo), cada una con su propio puntaje de 0 a 100, más un puntaje y estado general (*Saludable*, *En observación*, *En riesgo*).
- **Recomendaciones Personalizadas:** Sugerencias generadas por IA para cada dimensión, más una recomendación general.
- **Gamificación:** Sistema de medallas y logros que premian rachas de uso, mejoras en el balance financiero y buenos hábitos de ahorro.
- **Visualización Dinámica:** Paneles interactivos con gráficas financieras para el análisis visual de tendencias.

## Cómo Funciona
1. El usuario se registra e inicia sesión, y registra sus ingresos y transacciones.
2. El backend en Spring Boot valida la integridad de los datos y los almacena en una base de datos PostgreSQL.
3. Cuando el usuario solicita su análisis, el backend envía sus datos financieros a un **microservicio externo de Inteligencia Artificial** (desarrollado en Python), que se encarga de clasificar las transacciones y calcular el perfil financiero.
4. El backend recibe la respuesta del microservicio, la almacena, y la expone a través de su propia API REST.
5. El frontend consume esa API y renderiza visualmente los resultados, las gráficas y las medallas obtenidas.

## Requisitos Mínimos del MVP (Checklist de Cumplimiento)
- [x] **Motor de clasificación y análisis financiero:** Implementado como microservicio independiente en Python.
- [x] **Validación de entrada:** Validaciones con `@Valid` en los DTOs de entrada, rechazando montos inconsistentes o campos vacíos.
- [x] **Clasificación funcional de las transacciones:** Clasificación automática dentro de las categorías del negocio.
- [x] **Análisis del perfil financiero:** Determinación del estado del cliente en 4 dimensiones (Saludable / En observación / En riesgo).
- [x] **Generación de recomendaciones:** Mensajes accionables por dimensión, más una recomendación general.
- [x] **API documentada:** Endpoints expuestos mediante Swagger / OpenAPI (`springdoc-openapi`).
- [x] **Infraestructura en la nube:** Implementado con **Render**, con **PostgreSQL** como base de datos de producción.
- [x] **Mínimo de tres ejemplos reales de uso:** Perfiles de prueba precargados (ahorrador saludable, promedio en observación, endeudado en riesgo).

## Arquitectura Tecnológica

### Backend
- **Tecnología:** Java 17+ + Spring Boot.
- **Responsabilidades:**
  - API REST documentada con **Swagger / OpenAPI**, para la gestión de usuarios, ingresos, transacciones, análisis financiero y medallas.
  - Endpoints principales:
    - `POST /api/auth/login`: Inicio de sesión y creación automática de usuario.
    - `POST /api/movimientos/usuario/{usuarioId}` y `GET/PUT/DELETE`: gestión de transacciones (CRUD completo).
    - `POST /api/ingresos/usuario/{usuarioId}` y `GET/PUT/DELETE`: gestión de ingresos (CRUD completo).
    - `POST /api/analisis/analizar`: análisis financiero completo, delegando la clasificación y el cálculo al microservicio de IA.
    - Endpoints de `/api/medallas` para consultar los logros del usuario.
  - **Manejo de Errores y Validación:** Validaciones estrictas en los DTOs de entrada (`@Valid`), junto con un manejador global de excepciones (`@RestControllerAdvice`) que responde con códigos HTTP semánticos (ej. `400 Bad Request`) y mensajes estructurados.
  - Persistencia en **PostgreSQL** en producción (con H2 como base de datos de respaldo/desarrollo local).

### Módulo de IA y Ciencia de Datos
- **Tecnología:** Python, desplegado como **microservicio independiente**, consumido por el backend vía peticiones HTTP.
- **Responsabilidades:**
  - Clasificación automática de transacciones (tipo y categoría) a partir de su descripción.
  - Cálculo del perfil financiero en 4 dimensiones, con puntuación 0-100.
  - Generación de recomendaciones personalizadas por dimensión y general.

### Frontend
- **Tecnología:** HTML5, CSS3, JavaScript + Bootstrap.
- **Librerías de Visualización:** Chart.js para gráficas interactivas.
- **Responsabilidades:**
  - Interfaz para el registro de ingresos y transacciones.
  - Dashboard con métricas clave, distribución de gastos por categoría y medallas obtenidas.
  - Renderizado de las recomendaciones generadas por la IA.

### Infraestructura y Despliegue
- **Backend y microservicio de IA:** Desplegados en **Render**.
- **Base de datos:** **PostgreSQL**, desplegada también como servicio administrado en **Render**.

## Valor para el Cliente
- **Autonomía Financiera:** Herramienta directa que empodera al usuario en la toma de decisiones diarias.
- **Análisis en Profundidad:** El usuario no recibe solo un resultado genérico — entiende su situación desde 4 ángulos distintos, incluyendo el costo real de su deuda, no solo el monto.
- **Motivación:** El sistema de medallas convierte el cuidado de las finanzas personales en un hábito gratificante, no en una obligación.

## Estructura de Datos

### Entidad Usuario
- `id` (UUID)
- `username` / `password` (autenticación)
- `nombre`, `email`
- `ingresoMensual` (Numeric, opcional)
- Relación con sus medallas obtenidas

### Entidad Transaccion
- `id` (UUID)
- `usuario` (FK)
- `fecha`, `descripcion`, `monto`
- `formaPago` (Efectivo, Transferencia bancaria, Tarjeta de débito, Tarjeta de crédito)
- `tasaDeInteresDeLaTarjeta` (solo si es tarjeta de crédito)
- `tipoFinanciero` (Consumo / Pago de deuda / Ahorro e inversión)
- `categoria` (solo si el tipo es Consumo)

### Entidad Ingreso
- `id` (UUID)
- `usuario` (FK)
- `fecha`, `descripcion`, `monto`

### Entidad Medalla
- `id`, `codigo`, `nombre`, `descripcion`, `puntos`, `iconoUrl`

## Criterios de Éxito y Calidad Técnico-Funcional
- **Validación Robusta:** El sistema rechaza datos inconsistentes devolviendo respuestas JSON estructuradas y descriptivas ante fallos.
- **Precisión del Análisis:** Respuestas coherentes con el perfil financiero cargado, evaluadas bajo los 3 escenarios de prueba mínimos del proyecto.
- **Documentación Accesible:** Toda la API es explorable y probable directamente desde Swagger UI.

## Mensaje Resumen
Team 68 propone FinanceAI, una app de educación financiera que combina clasificación automática de transacciones mediante IA, un análisis financiero en 4 dimensiones con recomendaciones personalizadas, y un sistema de gamificación que motiva al usuario a mejorar sus hábitos — transformando datos financieros dispersos en decisiones claras y accionables.

