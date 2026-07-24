# Fase 1. Preparación del proyecto
## 1. Construcción del conjunto de datos de prueba

Crear entre 10 y 15 archivos JSON que representen distintos perfiles financieros.

Usuario con buen ahorro.
Usuario altamente endeudado.
Usuario con múltiples ingresos.
Usuario con alto gasto discrecional.
Usuario con bajo ingreso.
Usuario con muchas suscripciones digitales.
Usuario con inversiones.
Usuario con pocos movimientos.
Usuario con comportamiento financiero saludable.
Usuario en riesgo financiero.

Estos casos servirán durante todo el desarrollo para validar el funcionamiento del sistema.

## 2. Implementar la recepción del JSON

En modo de pruebas:

seleccionar aleatoriamente uno de los JSON de prueba;
cargarlo en memoria.

Posteriormente esta función podrá reemplazarse por la recepción desde una API.

## 3. Implementar la validación del JSON
Comprobar:

- campos obligatorios
- tipos de datos
- valores válidos
- estructura correcta

## 4. Construcción del objeto interno

Transformar el JSON recibido en el objeto con el que trabajará todo el motor.

Este objeto será el que se irá enriqueciendo durante todo el proceso.

# Fase 2. Clasificación de transacciones

## 5. Implementar el motor de clasificación

Clasificar cada transacción en:

- Consumo.
- Pago de deuda.
- Ahorro e inversión.

Actualizar el objeto interno.

## 6. Clasificar las transacciones de consumo

Asignar la categoría correspondiente:

- Vivienda.
- Alimentación.
- Transporte.
- Salud.
- Educación.
- Entretenimiento y ocio.
- Suscripciones digitales.
- Compras personales.
- Viajes y vacaciones.
- Otros.

Actualizar nuevamente el objeto.

## 7. Asignar el grupo funcional

Para las transacciones de consumo.

Asignar:

- Esencial.
- Discrecional.

Actualizar el objeto.

# Fase 3. Motor de análisis financiero

## 8. Construcción del motor de variables derivadas

Calcular:

- ingreso mensual
- consumo total
- pago de deuda
- ahorro e inversión
- egreso total
- balance mensual
- gasto por categoría
- distribución porcentual
  
## 9. Construcción del motor de indicadores

Aquí se calcularan los indicadores de todas las dimensiones.

## 10. Construcción del sistema de scoring

Definir:

- pesos de indicadores
- puntuación de cada dimensión
- rangos de estados
- recomendaciones

Este módulo será independiente de los indicadores.

## 11. Evaluación de Balance Financiero

Obtener:

- indicadores
- puntuación
- estado
- recomendaciones

## 12. Evaluación de Capacidad de Ahorro

Obtener:

- indicadores
- puntuación
- estado
- recomendaciones

## 13. Evaluación de Endeudamiento

Obtener:

- indicadores
- puntuación
- estado
- recomendaciones

## 14. Evaluación de Comportamiento de Consumo

Además del scoring:

perfil de consumo.

# Fase 4. Integración

## 15. Construcción del perfil financiero

Recibir las cuatro dimensiones.

Calcular:

- puntuación global
- estado global
- construcción del prompt para el LLM
- generación de la recomendación personalizada
  
## 16. Construcción de la respuesta

Crear el objeto de salida.

## 17. Conversión al JSON final

Generar el JSON exactamente con la estructura definida.

# Fase 5. Validación

## 18. Pruebas del sistema

Ejecutar los 15 casos de prueba.

Verificar:

clasificación;
indicadores;
scoring;
recomendaciones;
JSON final.

Corregir inconsistencias.

# Notas de diseño

## Uso de IA

|Componente	| Responsable |	IA |
| -- | -- | -- |
|Clasificación de transacciones|	LLM	|✅|
|Variables derivadas	|Motor financiero	|❌|
|Indicadores	|Motor financiero|	❌|
|Scoring|	Motor financiero|	❌|
|Estados|	Motor financiero|	❌|
|Recomendaciones por dimensión|	Motor financiero (reglas)|	❌|
|Perfil financiero|	Motor financiero	|❌|
|Recomendación final personalizada|	LLM|	✅|

