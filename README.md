# Team 68 - App de Educación Financiera

## Descripción del Proyecto
Team 68 es una aplicación de educación financiera enfocada en ayudar a los usuarios a entender y mejorar sus hábitos de consumo mediante el análisis inteligente de sus datos transaccionales y su perfil financiero.

La plataforma permite registrar ingresos y gastos por categorías, analizar el comportamiento financiero con Inteligencia Artificial y generar sugerencias prácticas de presupuesto, prioridades de gasto y estrategias de ahorro.

## Objetivo
Ofrecer una herramienta simple, intuitiva y confiable para:
- Organizar ingresos y gastos personales.
- Detectar patrones de consumo y comportamientos de riesgo.
- Recibir recomendaciones personalizadas basadas en datos reales para una mejor salud financiera.

## Características Principales
- **Registro de Ingresos y Gastos:** Control detallado de movimientos con categorización flexible.
- **Clasificación Automática de Transacciones:** Agrupación inteligente de movimientos en categorías clave (vivienda, transporte, alimentación, ocio, ahorro, salud y educación).
- **Análisis del Comportamiento y Clasificación del Perfil Financiero:** Evaluación automatizada que clasifica al usuario en un perfil determinado (*Saludable*, *En observación*, *En riesgo* o *Con una probabilidad*) acompañado de su correspondiente nivel o probabilidad de certeza.
- **Visualización Dinámica:** Paneles interactivos con gráficas financieras para el análisis visual de tendencias.
- **Recomendaciones de Presupuesto Mensual:** Sugerencias automatizadas y accionables ajustadas a la realidad de cada usuario.

## Cómo Funciona
1. El usuario registra sus ingresos, gastos y actualiza los datos de su perfil financiero.
2. El backend en Spring Boot valida la integridad de los datos y los almacena de forma segura.
3. El motor de IA (embebido en el backend vía ONNX Runtime) procesa los datos históricos y las variables del perfil.
4. El sistema genera respuestas en formato JSON con sugerencias de presupuesto y alertas de riesgo.
5. El frontend renderiza visualmente los resultados y las gráficas mediante librerías de JavaScript.

## Requisitos Mínimos del MVP (Checklist de Cumplimiento)
- [ ] **Modelo entrenado y cargado correctamente:** Motor predictivo operacional cargado de forma nativa.
- [ ] **Validación de entrada:** Robustez ante datos erróneos, montos negativos o campos vacíos.
- [ ] **Clasificación funcional de las transacciones:** Clasificación correcta dentro de las categorías del negocio.
- [ ] **Análisis del perfil financiero:** Determinación del estado del cliente (Saludable / En observación / En riesgo).
- [ ] **Generación de recomendaciones:** Mensajes accionables y lógicos según las métricas obtenidas.
- [ ] **API documentada:** Endpoints completamente expuestos mediante Swagger / OpenAPI.
- [ ] **Integración con OCI:** Infraestructura en la nube utilizando servicios mínimos obligatorios.
- [ ] **Mínimo de tres ejemplos reales de uso:** Casos prácticos integrados para la evaluación inmediata del jurado.

## Arquitectura Tecnológica

### Backend (Monolito Robusto)
- **Tecnología:** Java 17+ + Spring Boot 3.x.
- **Responsabilidades:**
  - API REST completamente documentada mediante **Swagger / OpenAPI** para la gestión integral de usuarios y movimientos.
  - Implementación obligatoria de los siguientes endpoints exigidos por el brief:
    - `POST /analisis-financiero`: Endpoint centralizado que procesa las variables de perfil financiero e históricos para determinar la salud financiera y generar las recomendaciones.
    - `POST /clasificacion-transacciones`: Endpoint dedicado a la catalogación inteligente e inmediata de transacciones.
  - **Manejo de Errores y Validación:** Filtros estrictos en los esquemas de entrada de datos (`@Valid`) acoplados a un controlador central de excepciones (`@RestControllerAdvice`) para interceptar solicitudes con montos inconsistentes o datos vacíos, respondiendo siempre con códigos de estado HTTP semánticos (ej. `400 Bad Request`).
  - Ejecución nativa del modelo predictivo mediante la librería **ONNX Runtime**, eliminando la necesidad de microservicios externos en Python y optimizando el consumo de infraestructura.

### Módulo de IA y Ciencia de Datos
- **Tecnología:** Python (Fase de Desarrollo y Entrenamiento) -> Exportado a formato **ONNX**.
- **Responsabilidades:**
  - Creación y simulación del dataset financiero base utilizando técnicas de generación de datos sintéticos.
  - Análisis descriptivo y predictivo de datos históricos transaccionales.
  - Clasificación de perfiles de riesgo financiero a partir de variables estrictas del modelo.

### Frontend
- **Tecnología:** HTML5, CSS3, JavaScript Moderno + Bootstrap 5.
- **Librerías de Visualización:** Chart.js (gráficos interactivos de pastel y tendencias lineales).
- **Responsabilidades:**
  - Interfaz responsiva y accesible para la carga sin fricciones de transacciones.
  - Dashboard centralizado con métricas clave y distribución de gastos por categorías.
  - Renderizado claro de las sugerencias generadas por la IA utilizando un lenguaje amigable y directo.

### Infraestructura (Oracle Cloud Infrastructure - OCI)
Optimizada para la capa *Always Free* de Oracle:
- **OCI Compute:** Instancia de máquina virtual asignada para el despliegue del contenedor del backend y frontend.
- **OCI Autonomous Database:** Base de datos relacional administrada (Oracle Autonomous Transaction Processing) para la persistencia segura de usuarios, transacciones y bitácoras de recomendaciones.
- **OCI Object Storage:** Almacenamiento de objetos para resguardar los archivos `.onnx` del modelo entrenado y los backups del sistema.

## Valor para el Cliente
- **Autonomía Financiera:** Herramienta directa que empodera al usuario en la toma de decisiones diarias.
- **Inteligencia al Instante:** Recomendaciones predictivas sin latencia gracias a la integración embebida del modelo ONNX.
- **Estructura Escalable:** Arquitectura limpia en la nube que permite añadir nuevos modelos predictivos y reglas de negocio complejas sin reestructurar el núcleo del sistema.

## Estructura de Datos (Esquema para la IA)

### Entidad Usuario / Perfil Financiero
- `id_usuario` (UUID)
- `nombre` (String)
- `email` (String)
- `ingreso_mensual` (Numeric) *[Campo Obligatorio]*
- `frecuencia_ahorro` (String: mensual, quincenal, ocasional) *[Campo Obligatorio]*
- `nivel_de_endeudamiento` (Numeric / Porcentaje) *[Campo Obligatorio]*
- `fecha_registro` (Timestamp)

### Entidad Movimiento / Transacción
- `id_movimiento` (UUID)
- `id_usuario` (UUID - FK)
- `tipo` (Enum: INGRESO | GASTO)
- `categoria` (String: vivienda, transporte, alimentación, ocio, ahorro, salud, educación) *[Campos del Brief]*
- `monto` (Numeric - Validado positivo)
- `fecha` (Date)
- `descripcion` (String)

### Entidad Recomendación
- `id_recomendacion` (UUID)
- `id_usuario` (UUID - FK)
- `periodo` (String: MM-AAAA)
- `perfil_calculado` (Enum: SALUDABLE | EN_OBSERVACION | EN_RIESGO) *[Campo Obligatorio]*
- `tipo_recomendacion` (Enum: PRESUPUESTO | PRIORIDAD_GASTO | ALERTA_RIESGO)
- `mensaje` (Text)
- `nivel_confianza` (Numeric / Float que representa la probabilidad del perfil) *[Campo Obligatorio]*

## Criterios de Éxito y Calidad Técnico-Funcional
- **Cero Fricción:** El usuario registra y visualiza sus finanzas en menos de 3 clics desde la interfaz principal.
- **Validación Robusta:** El sistema rechaza datos inconsistentes devolviendo respuestas JSON estructuradas y descriptivas ante fallos.
- **Precisión Predictiva:** Respuestas del modelo JSON coherentes con el perfil financiero cargado, evaluadas bajo los 3 escenarios de prueba mínimos del proyecto.
- **Eficiencia en la Nube:** Despliegue completo y funcional operando de forma estable bajo los recursos controlados de la capa gratuita de OCI.

## Mensaje Resumen
Team 68 propone una App de Educación Financiera que unifica la gestión transaccional diaria, la analítica predictiva mediante IA embebida y una visualización de datos moderna en la nube de Oracle, transformando la contabilidad tradicional en decisiones financieras inteligentes y accionables.
