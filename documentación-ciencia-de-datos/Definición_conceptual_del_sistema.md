# Objetivo del sistema:

Desarrollar un sistema inteligente capaz de analizar el comportamiento financiero de un usuario a partir de información relacionada con sus ingresos, gastos, ahorro y endeudamiento,
con el fin de identificar patrones financieros, evaluar su salud financiera, clasificar su perfil y generar recomendaciones personalizadas que apoyen la toma de decisiones.

# Definición de salud financiera:

La salud financiera es la capacidad de una persona para administrar sus recursos económicos de manera equilibrada y sostenible, 
manteniendo un balance adecuado entre ingresos, gastos, ahorro y endeudamiento, de forma que pueda satisfacer sus necesidades actuales sin comprometer su estabilidad financiera futura.

# Dimensiones principales de la salud financiera:

## 1. Balance financiero
¿La persona vive dentro de sus posibilidades?
Aquí analizamos si los ingresos son suficientes para cubrir gastos y obligaciones.
Esta dimensión debería ser la más importante.
Sin equilibrio financiero es difícil que exista una buena salud financiera.

## 2. Capacidad de ahorro
¿La persona genera recursos para el futuro?
No solo queremos saber si ahorró.
Queremos saber si realmente tiene capacidad para ahorrar.
Esto mide estabilidad y preparación para imprevistos.

## 3. Endeudamiento
¿La deuda es saludable respecto a su capacidad económica?
No queremos castigar cualquier deuda.
Queremos evaluar si la deuda es manejable.
Esta dimensión ayuda a identificar riesgos financieros.

## 4. Comportamiento de consumo
¿Cómo utiliza su dinero?
Aquí aparecen aspectos como:
- distribución del gasto,
- categorías predominantes,
- gastos recurrentes,
- gastos discrecionales,
- concentración del gasto.

# Estados posibles de cada dimensión:
🟢 Saludable
🟡 En observación
🔴 En riesgo

Ejemplo:

|Dimensión|Estado|
|---|---|
|Balance financiero|Saludable|
|Capacidad de ahorro|En observación|
|Endeudamiento|Saludable|
|Comportamiento de consumo|En riesgo|

# Escala de puntuación

Además de clasificar el resultado de cada dimensión y del perfil financiero general mediante los estados Saludable, En observación y En riesgo, el sistema incorporará una escala de puntuación de 0 a 100. Esta puntuación tiene como objetivo ofrecer una evaluación más precisa del desempeño financiero del usuario y facilitar la interpretación de los resultados.

La puntuación será calculada a partir de un sistema de scoring basado en los indicadores financieros definidos para cada dimensión. Cada indicador contribuirá al resultado mediante un peso previamente establecido, permitiendo obtener una calificación numérica que represente el nivel de desempeño del usuario en esa dimensión.

Una vez calculada la puntuación, el sistema asignará el estado correspondiente de acuerdo con rangos previamente definidos. De esta manera, el estado cualitativo será una interpretación de la puntuación obtenida y no un resultado independiente.

Este enfoque ofrece varias ventajas:

- Proporciona una evaluación más detallada que una clasificación únicamente cualitativa.
- Permite identificar pequeñas mejoras o deterioros en la salud financiera del usuario.
- Facilita la comparación entre distintas evaluaciones realizadas en diferentes periodos.
- Mantiene un criterio de evaluación transparente y explicable, ya que la puntuación se obtiene directamente a partir de los indicadores financieros y de las reglas de scoring definidas por el sistema.

Cada una de las cuatro dimensiones generará tanto una puntuación como un estado, mientras que el perfil financiero general se obtendrá integrando los resultados de todas las dimensiones mediante un sistema de ponderación.

**Ejemplo de resultados:**
| Elemento |	Puntuación |	Estado |
| -- | -- | -- |
| Balance Financiero	| 87	| Saludable |
| Capacidad de Ahorro |	64	| En observación |
| Endeudamiento |	91	| Saludable |
| Comportamiento de Consumo	| 58	| En observación |
| **Perfil Financiero**	| **75** |	**En observación** |

# Perfil Financiero General

El perfil financiero general representa la evaluación integral de la salud financiera del usuario. Su objetivo es sintetizar el desempeño obtenido en cada una de las cuatro dimensiones analizadas por el sistema en una única puntuación y un estado general.

A diferencia del scoring de cada dimensión, el cual se calcula a partir de indicadores financieros específicos, el scoring del perfil financiero general se obtiene utilizando como entrada las puntuaciones finales de las cuatro dimensiones:

- Balance Financiero.
- Capacidad de Ahorro.
- Endeudamiento.
- Comportamiento de Consumo.

Cada una de estas dimensiones genera previamente una puntuación en una escala de 0 a 100, la cual resume el desempeño del usuario dentro de esa área específica. Posteriormente, dichas puntuaciones son combinadas mediante un sistema de ponderación para calcular la puntuación final del perfil financiero.

## Sistema de ponderación

Para calcular la puntuación final, cada dimensión tendrá un peso que representará su importancia relativa dentro de la evaluación global de la salud financiera. Estos pesos serán definidos durante el diseño del sistema y deberán sumar el 100 %.

La ponderación permite reflejar que algunas dimensiones pueden tener una mayor influencia sobre la salud financiera general que otras, manteniendo un criterio de evaluación consistente y transparente.

## Resultado del scoring

Como resultado de este proceso, el sistema generará:

- Una puntuación final en una escala de 0 a 100.
- Un estado general del perfil financiero, obtenido a partir de los rangos de puntuación definidos por el sistema.

## Estados generales posibles

🟢 Saludable
🟡 En observación
🔴 En riesgo

De esta manera, el perfil financiero ofrecerá tanto una evaluación cuantitativa como una interpretación cualitativa de la situación financiera del usuario.

# Analisis profundo de cada dimension:

## Dimensión 1 — BALANCE FINANCIERO
El balance financiero evalúa la capacidad de una persona para cubrir sus obligaciones económicas con los ingresos que percibe durante un periodo determinado, 
permitiendo identificar si existe un equilibrio, un superávit o un déficit financiero.

### ¿Qué preguntas debe responder?
- ¿Los ingresos son suficientes para cubrir los gastos del periodo?
- ¿Después de cubrir todas las obligaciones queda dinero disponible?
- ¿La persona está viviendo por encima de sus posibilidades?
- ¿Qué porcentaje del ingreso está comprometido por los gastos?

### Variables necesarias
- Ingreso mensual: Suma de todos los ingresos
- Consumo total mensual: Suma de las transacciones clasificadas como consumo.
- Pago mensual de deudas: Suma de las transacciones clasificadas como pago de deuda.
- Egreso total: consumo total mensual + pago mensual de deudas

### Indicadores generados
- Balance mensual: Determinar cuánto dinero permanece disponible después de cubrir todos los egresos. Determina si existe superávit, equilibrio o déficit financiero.
  (Balance mensual = Ingreso mensual − Egreso total)
- Tasa de gasto: Determinar qué proporción del ingreso se utiliza para cubrir los egresos. Mide la presión financiera ejercida por los egresos.
  (Tasa de gasto = Egreso total / Ingreso mensual)
- Margen financiero: Medir qué porcentaje del ingreso permanece disponible una vez cubiertos todos los egresos. Evalúa la capacidad de maniobra económica del usuario.
  (Margen financiero = Balance mensual / Ingreso mensua)

### Resultados posibles de acuerdo a los indicadores

#### Saludable
Justificación:
- Balance mensual positivo.
- Tasa de gasto moderada.
- Margen financiero adecuado.

#### En observación

Justificación:
- Balance mensual positivo.
- Sin embargo, la tasa de gasto es elevada.
- El margen financiero es reducido.

#### En riesgo

Justificación:
- Balance mensual negativo.
- Los egresos superan los ingresos.
- No existe margen financiero.


## Dimensión 2 — CAPACIDAD DE AHORRO
La capacidad de ahorro evalúa la habilidad del usuario para reservar una parte de sus ingresos de forma constante, después de cubrir sus obligaciones económicas, con el fin de fortalecer su estabilidad financiera y prepararse para necesidades futuras.

### Notas importantes
El ahorro no se calculará como el dinero sobrante al final del periodo.
Solo se considerará ahorro el dinero que el usuario destine explícitamente a instrumentos o cuentas de ahorro e inversión.
El ahorro implícito (dinero disponible no gastado) no formará parte de los indicadores de esta dimensión.

### ¿Qué preguntas debe responder?
- ¿El usuario logra ahorrar parte de sus ingresos?
- ¿Qué porcentaje de sus ingresos destina al ahorro?
- ¿El ahorro es suficiente para fortalecer su estabilidad financiera?
- ¿Existe capacidad real de ahorro después de cubrir todos los egresos?
  
### Variables necesarias

- Ahorro e inversión total: Suma de todas las transacciones clasificadas como ahorro o inversión.
- Balance mensual: Resultado obtenido en la dimensión Balance Financiero.
- Margen financiero:	Resultado obtenido en la dimensión Balance Financiero.
  
### Indicadores generados
- Tasa de ahorro: Determinar qué porcentaje del ingreso mensual se destina al ahorro o la inversión. Mide el esfuerzo de ahorro del usuario.
Permite comparar usuarios con distintos niveles de ingreso. (Tasa de ahorro = Ahorro e inversión total / Ingreso mensual)

- Ahorro e inversión del periodo: Determinar el monto absoluto destinado al ahorro o la inversión durante el periodo. Cuantifica el esfuerzo económico realizado.
Complementa la tasa de ahorro. (Ahorro e inversión del periodo = Suma de transacciones clasificadas como ahorro o inversión)

- Aprovechamiento del margen financiero: Evalúa si el usuario aprovecha su capacidad real de ahorro. (Aprovechamiento del margen = Ahorro e inversión total / Balance mensual)
  
### Resultados posibles de acuerdo a los indicadores

#### Saludable

Justificación:
La tasa de ahorro representa una parte importante de los ingresos.
Existe un ahorro o inversión constante durante el periodo.
Se aprovecha adecuadamente el margen financiero disponible.

#### En observación

Justificación:

El usuario realiza ahorro o inversión, pero el porcentaje es reducido.
El monto ahorrado es bajo respecto a su capacidad económica.
Solo una pequeña parte del margen financiero se destina al ahorro.

#### En riesgo

Justificación:

No existen transacciones de ahorro o inversión.
La tasa de ahorro es nula o muy baja.
El margen financiero disponible no se aprovecha para construir estabilidad financiera.

## Dimensión 3 — ENDEUDAMIENTO

Evaluar si las obligaciones financieras del usuario son sostenibles de acuerdo con sus ingresos y su capacidad de pago, identificando el nivel de riesgo que representan para su estabilidad financiera.

### ¿Qué preguntas debe responder?

- ¿Qué porcentaje de los ingresos se destina al pago de deudas?
- ¿Las obligaciones financieras representan una carga excesiva?
- ¿El usuario mantiene un nivel de endeudamiento sostenible?
- ¿El pago de las deudas compromete su estabilidad financiera?

### Variables necesarias

- Pago mensual de deudas:	Suma de las transacciones clasificadas como pago de deuda.
- Balance mensual:	Proveniente de la dimensión Balance Financiero.
- Egreso total:	Proveniente de la dimensión Balance Financiero.

### Indicadores generados

- Ratio de endeudamiento: Determinar qué porcentaje del ingreso mensual se destina al pago de obligaciones financieras. Evalúa la carga financiera respecto al ingreso.
Permite comparar usuarios con distintos niveles de ingreso. Indica qué tan sostenible es el pago de las obligaciones financieras. (Ratio de endeudamiento = Pago mensual de deudas / Ingreso mensual)

- Monto destinado al pago de deudas: Determinar el monto absoluto destinado al pago de obligaciones financieras durante el periodo. Cuantifica el esfuerzo económico destinado al cumplimiento de obligaciones financieras. Complementa al ratio de endeudamiento mostrando el valor monetario destinado al pago de deudas. (Monto destinado al pago de deudas = Suma de transacciones clasificadas como pago de deuda)

- Presión de la deuda: Evaluar qué proporción del gasto total corresponde al pago de obligaciones financieras.Mide qué tan dominante es la deuda dentro del presupuesto mensual.
Permite identificar cuando el pago de obligaciones comienza a desplazar otros gastos importantes. Complementa el análisis del ratio de endeudamiento desde la perspectiva del gasto total. (Presión de la deuda = Pago mensual de deudas / Egreso total)

### Resultados posibles de acuerdo a los indicadores

#### Saludable

Justificación:
- El ratio de endeudamiento es bajo.
- El monto destinado al pago de deudas es consistente con el nivel de ingresos.
- La deuda representa una pequeña proporción del presupuesto mensual.

#### En observación

Justificación:
- El ratio de endeudamiento comienza a ser elevado.
- Una parte importante del presupuesto se destina al pago de deudas.
- La presión de la deuda reduce la flexibilidad financiera del usuario.

#### En riesgo

Justificación:
- Una proporción elevada de los ingresos se destina al pago de deudas.
- El monto destinado al pago de obligaciones limita significativamente la capacidad financiera.
- La deuda domina el presupuesto mensual y compromete la estabilidad financiera.

## Dimensión 4 — COMPORTAMIENTO DE CONSUMO

Es el análisis de la forma en que el usuario distribuye sus gastos entre las diferentes categorías de consumo, permitiendo identificar patrones, hábitos y áreas donde existen oportunidades de mejorar la administración de sus recursos.

### ¿Qué preguntas debe responder?

- ¿En qué categorías concentra la mayor parte de sus gastos?
- ¿Cómo distribuye su presupuesto entre las distintas categorías?
- ¿Existen patrones de consumo relevantes?
- ¿Hay categorías que representan una proporción excesiva del gasto?
- ¿Qué hábitos de consumo pueden identificarse?

### Variables necesarias
- Consumo total mensual:	Suma de todas las transacciones clasificadas como consumo.
- Gasto por categoría:	Suma de las transacciones pertenecientes a cada categoría de consumo.
- Distribución porcentual del gasto:	Porcentaje que representa cada categoría respecto al consumo total.


### Indicadores generados

- Distribución del gasto por categorías: Determinar cómo se distribuye el consumo del usuario entre las distintas categorías de gasto. Permite conocer el peso relativo de cada categoría. Facilita comparar hábitos de consumo entre distintos usuarios. Constituye la base para identificar patrones de consumo.
- Índice de concentración del gasto: Evaluar qué tan equilibrada o concentrada se encuentra la distribución del consumo. Identifica si el presupuesto está distribuido entre diversas categorías. Detecta cuando una o pocas categorías concentran la mayor parte del consumo. Complementa la distribución porcentual del gasto. (Nota: La fórmula específica del índice se definirá posteriormente)
- Perfil de consumo: A partir de los indicadores financieros anteriores, el sistema generará un conjunto de indicadores interpretativos que describen el comportamiento de consumo del usuario. Estos indicadores serán utilizados tanto para la evaluación de la dimensión como para la generación de recomendaciones personalizadas.

Indicador de consumo 1: _Predominio del gasto_

Describe el tipo de necesidades hacia las que el usuario orienta la mayor parte de su presupuesto.

Posibles resultados:
- Predominio en gastos esenciales.
- Balance entre gastos esenciales y discrecionales.
- Predominio en gastos discrecionales.

Indicador de consumo 2: _Tipo de consumo_

Describe la forma en que se distribuye el gasto.

Posibles resultados:

- Consumo equilibrado.
- Consumo moderadamente concentrado.
- Consumo altamente concentrado.

Indicador de consumo 3: _Diversificación del consumo_

Describe si el usuario distribuye su presupuesto entre distintas categorías o concentra sus recursos en pocas de ellas.

Posibles resultados:

- Consumo diversificado.
- Consumo poco diversificado.

Indicador de consumo 4: _Categoría predominante_

Identifica la categoría que representa el mayor porcentaje del consumo.

Ejemplos:

- Alimentación.
- Vivienda.
- Transporte.
- Salud.
- Educación.
- Entretenimiento.
- Restaurantes.
- Compras.
- Etc.

Este indicador tiene un propósito descriptivo y servirá para personalizar las recomendaciones, sin afectar directamente la evaluación de la dimensión.

### Evaluación de la dimensión

La evaluación del Comportamiento de Consumo se realizará mediante un proceso de interpretación compuesto por dos etapas:

#### Etapa 1

Cálculo de los indicadores financieros:

- Distribución del gasto por categorías.
- Índice de concentración del gasto.

#### Etapa 2

Generación de los indicadores de consumo:

- Predominio del gasto.
- Tipo de consumo.
- Diversificación del consumo.
- Categoría predominante.

Con base en estos indicadores, la dimensión podrá clasificarse en uno de los siguientes estados:

🟢 Saludable
🟡 En observación
🔴 En riesgo

Los criterios de clasificación y el sistema de puntuación se definirán posteriormente.

### Resultados posibles de acuerdo a los indicadores

#### Saludable

Indicadores de consumo

- Predominio en gastos esenciales.
- Consumo equilibrado.
- Consumo diversificado.
- Categoría predominante: Vivienda.

Justificación

- El presupuesto se distribuye de forma equilibrada.
- No existe una concentración excesiva del gasto.
- La mayor parte del consumo se destina a necesidades esenciales.

#### En observación

Indicadores de consumo

- Balance entre gastos esenciales y discrecionales.
- Consumo moderadamente concentrado.
- Consumo poco diversificado.
- Categoría predominante: Entretenimiento.

Justificación

- Existe una concentración moderada del gasto.
- El consumo discrecional comienza a representar una parte importante del presupuesto.
- La distribución del gasto puede optimizarse.

#### En riesgo

Indicadores de consumo

- Predominio en gastos discrecionales.
- Consumo altamente concentrado.
- Consumo poco diversificado.
- Categoría predominante: Entretenimiento.

Justificación

- Una parte importante del presupuesto se concentra en gastos discrecionales.
- El consumo presenta poca diversificación.
- El comportamiento de consumo puede comprometer la estabilidad financiera.

# Resumen de variables necesarias y indicadores generados para el sistema funcione

## Variables de entrada (usuario)

- Ingreso mensual
- Transacciones financieras: Registro de todas las transacciones del periodo.

## Variables derivadas globales

|Variable|	Cómo se obtiene|
| --- | --- |
|Consumo total mensual|	Suma de transacciones de consumo.|
|Pago mensual de deudas|	Suma de transacciones clasificadas como deuda.|
|Ahorro e inversión total|	Suma de transacciones clasificadas como ahorro e inversión.|
|Gasto por categoría|	Suma por categoría de consumo.|
|Distribución porcentual del gasto|	Porcentaje de cada categoría respecto al consumo total.|
|Egreso total|	Consumo total + Pago de deudas.|

## Indicadores generados

|Dimensión	|Indicadores|
| --- | --- |
|Balance Financiero|	Balance mensual, Tasa de gasto, Margen financiero|
|Capacidad de Ahorro|	Tasa de ahorro, Ahorro e inversión del periodo, Aprovechamiento del margen financiero|
|Endeudamiento|	Ratio de endeudamiento, Monto destinado al pago de deudas, Presión de la deuda|
|Comportamiento de Consumo|	Distribución del gasto por categorías, Índice de concentración del gasto, Perfil de consumo|

## Perfil de consumo

Se generan únicamente para la cuarta dimensión.

|Elemento|	Posibles valores|
| --- | --- |
|Predominio del gasto|	Esenciales, Balanceado, Discrecionales|
|Tipo de consumo|	Equilibrado, Moderadamente concentrado, Altamente concentrado|
|Diversificación|	Diversificado, Poco diversificado|
|Categoría predominante|	Vivienda, Alimentación, Salud, etc.|


# Forma de clasificar las transacciones

Las transacciones se clasificaran en tres tipos financieros:
- Consumo
- Pago de deuda
- Ahorro e inversión

A su vez, las transacciones clasificadas como consumo se clasificaran en las siguientes categorias:

| Categoría	|Tipo|
| --- |--- |
|🏠 Vivienda|	Esencial|
|🍽️ Alimentación|	Esencial|
|🚗 Transporte|	Esencial|
|🏥 Salud	|Esencial|
|🎓 Educación|	Esencial|
|🎉 Entretenimiento y ocio|	Discrecional|
| :tv: Suscripciones digitales|	Discrecional|
|🛍️ Compras personales|	Discrecional|
|✈️ Viajes y vacaciones	|Discrecional|
|📦 Otros|	Depende del análisis o revisión|


# Resultados finales entregables del analisis

**Datos del usuario:** Identificador y nombre del usuario analizado.

**Perfil financiero:** Estado general de la salud financiera obtenido a partir de la evaluación conjunta de las cuatro dimensiones.

**Resultados por dimensión:**

- Estado de la dimensión.
- Indicadores financieros utilizados para su evaluación.
- Recomendaciones específicas de la dimensión.

**Perfil de consumo (únicamente para la dimensión Comportamiento de Consumo):**

- Distribución del gasto por categoría.
- Índice de concentración del gasto.
- Predominio del gasto.
- Tipo de consumo.
- Diversificación del consumo.
- Categoría predominante.
  
**Recomendaciones generales:** Conjunto de recomendaciones integrales generadas a partir del análisis de todas las dimensiones, orientadas a fortalecer la salud financiera del usuario.

# Ejemplo de ficha de datos de entrada

```
{
  "usuario": {
    "nombre": "Brayan Lira"
  },
  "periodo": {
    "inicio": "2026-07-01",
    "fin": "2026-07-31"
  },
  "ingresos": [
    {
      "descripcion": "Salario",
      "monto": 25000
    },
    {
      "descripcion": "Trabajo freelance",
      "monto": 4500
    },
    {
      "descripcion": "Rendimientos de inversión",
      "monto": 800
    }
  ],
  "transacciones": [
    {
      "fecha": "2026-07-02",
      "descripcion": "Walmart León",
      "monto": 1350
    },
    {
      "fecha": "2026-07-03",
      "descripcion": "Netflix",
      "monto": 219
    },
    {
      "fecha": "2026-07-05",
      "descripcion": "Pago tarjeta Santander",
      "monto": 3200
    },
    {
      "fecha": "2026-07-08",
      "descripcion": "CETES Directo",
      "monto": 1500
    }
  ]
}
```



# Ejemplo de ficha de datos de salida

```
{
  "usuario": {
    "id": 1,
    "nombre": "Brayan Lira"
  },
  "perfil_financiero": {
    "puntuacion": 76,
    "estado": "En observación",
    "dimensiones": {
      "balance_financiero": 87,
      "capacidad_ahorro": 64,
      "endeudamiento": 91,
      "comportamiento_consumo": 58
    }
  },
  "dimensiones": {
    "balance_financiero": {
      "puntuacion": 87,
      "estado": "Saludable",
      "indicadores": {
        "balance_mensual": 5500,
        "tasa_gasto": 0.78,
        "margen_financiero": 0.22
      },
      "recomendaciones": [
        "Mantener el equilibrio actual entre ingresos y gastos.",
        "Continuar monitoreando el margen financiero mensualmente."
      ]
    },
    "capacidad_ahorro": {
      "puntuacion": 64,
      "estado": "En observación",
      "indicadores": {
        "tasa_ahorro": 0.08,
        "ahorro_inversion_periodo": 2000,
        "aprovechamiento_margen": 0.36
      },
      "recomendaciones": [
        "Incrementar gradualmente el porcentaje destinado al ahorro.",
        "Aprovechar una mayor parte del margen financiero para ahorro e inversión."
      ]
    },
    "endeudamiento": {
      "puntuacion": 91,
      "estado": "Saludable",
      "indicadores": {
        "ratio_endeudamiento": 0.12,
        "pago_deudas": 3000,
        "presion_deuda": "Baja"
      },
      "recomendaciones": [
        "Mantener el nivel actual de endeudamiento.",
        "Evitar adquirir nuevas deudas innecesarias."
      ]
    },
    "comportamiento_consumo": {
      "puntuacion": 58,
      "estado": "En observación",
      "indicadores": {
        "distribucion_gasto_categoria": {
          "Vivienda": 30.2,
          "Alimentación": 21.8,
          "Transporte": 12.5,
          "Salud": 4.8,
          "Educación": 6.5,
          "Entretenimiento y ocio": 15.4,
          "Suscripciones digitales": 6.1,
          "Compras personales": 2.7,
          "Viajes y vacaciones": 0.0,
          "Otros": 0.0
        },
        "indice_concentracion": 0.58
      },
      "perfil_consumo": {
        "predominio_gasto": "Balance entre gastos esenciales y discrecionales",
        "tipo_consumo": "Moderadamente concentrado",
        "diversificacion_consumo": "Diversificado",
        "categoria_predominante": "Vivienda"
      },
      "recomendaciones": [
        "Reducir gradualmente el gasto en entretenimiento y ocio.",
        "Revisar las suscripciones digitales activas y cancelar aquellas con poco uso.",
        "Mantener una distribución equilibrada entre gastos esenciales y discrecionales.",
        "Continuar monitoreando la distribución del presupuesto."
      ]
    }
  },
  "recomendaciones_generales": [
    "Incrementar la capacidad de ahorro para fortalecer la estabilidad financiera.",
    "Mantener el bajo nivel de endeudamiento actual.",
    "Revisar periódicamente los gastos discrecionales para mejorar el margen financiero."
  ]
}
```

# Uso de Inteligencia Artificial dentro de la arquitectura del sistema

Con el objetivo de desarrollar un sistema confiable, transparente y fácilmente explicable, se adoptará una arquitectura híbrida en la que la Inteligencia Artificial será utilizada únicamente en aquellas tareas donde aporta un valor significativo, mientras que la metodología de evaluación financiera permanecerá completamente definida mediante reglas de negocio implementadas por el equipo de desarrollo.

Este enfoque permite aprovechar las fortalezas de la IA sin perder el control sobre la lógica financiera del sistema.

## Clasificación automática de transacciones

La primera etapa en la que se incorporará Inteligencia Artificial corresponde a la clasificación automática de las transacciones financieras.

A partir de la descripción de cada transacción, un modelo de lenguaje (LLM) identificará:

- El tipo principal de la transacción:
  - Consumo.
  - Pago de deuda.
  - Ahorro e inversión.
- En caso de tratarse de una transacción de consumo, determinará además su categoría correspondiente:
  - Vivienda.
  - Alimentación.
  - Transporte.
  - Salud.
  - Educación.
  - Entretenimiento y ocio.
  - Restaurantes y comida fuera.
  - Compras personales.
  - Viajes y vacaciones.
  - Otros.

Posteriormente, el sistema asignará automáticamente el grupo funcional correspondiente (Esencial o Discrecional) de acuerdo con la categoría identificada.

La utilización de un LLM en esta etapa permite interpretar descripciones de transacciones escritas en lenguaje natural, incluso cuando presentan abreviaturas, nombres comerciales o formatos diferentes según la institución financiera.

## Motor de análisis financiero

Una vez clasificadas las transacciones, todo el proceso de evaluación financiera será realizado exclusivamente por el motor desarrollado por el equipo.

Esta parte del sistema no dependerá de modelos de Inteligencia Artificial ni de aprendizaje automático, sino de una metodología basada en reglas de negocio previamente definidas.

El motor será responsable de:

- Calcular las variables derivadas.
- Calcular los indicadores financieros de cada dimensión.
- Aplicar el sistema de scoring de cada dimensión.
- Determinar la puntuación de cada dimensión.
- Asignar el estado correspondiente.
- Calcular el scoring del perfil financiero general.
- Determinar el estado general del perfil financiero.
- Seleccionar las recomendaciones aplicables de acuerdo con los resultados obtenidos.

Este enfoque garantiza que todos los resultados sean consistentes, reproducibles y completamente explicables.

## Generación de recomendaciones en lenguaje natural

Las recomendaciones serán determinadas inicialmente mediante reglas de negocio implementadas dentro del motor de análisis financiero.

Es decir, el sistema decidirá qué acciones deben recomendarse al usuario con base en los indicadores, puntuaciones y estados obtenidos durante la evaluación.

Posteriormente, un modelo de lenguaje (LLM) tendrá como única responsabilidad transformar ese conjunto de recomendaciones en un texto más natural, claro y personalizado para el usuario.

De esta manera, el modelo de lenguaje no tomará decisiones financieras ni modificará la lógica del sistema; únicamente actuará como un componente encargado de mejorar la comunicación de los resultados.

En conjunto, esta estrategia convierte a la Inteligencia Artificial en una herramienta de apoyo para tareas de interpretación y comunicación, mientras que la evaluación financiera permanece sustentada en una metodología transparente, consistente y completamente controlada por el sistema desarrollado por el equipo.



                   

                 

