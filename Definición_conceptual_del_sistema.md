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
- Ingreso mensual
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
|🍔 Restaurantes y comida fuera|	Discrecional|
|🛍️ Compras personales|	Discrecional|
|✈️ Viajes y vacaciones	|Discrecional|
|📦 Otros|	Depende del análisis o revisión|

# Perfil Financiero 

El perfil financiero representa el resultado integral del análisis realizado por el sistema sobre la información financiera del usuario durante un periodo determinado. Este perfil se construye a partir de la evaluación de cuatro dimensiones fundamentales: balance financiero, capacidad de ahorro, endeudamiento y comportamiento de consumo. Cada dimensión es analizada mediante indicadores específicos que permiten determinar su estado, identificar fortalezas y áreas de oportunidad, y generar recomendaciones personalizadas. Como resultado, el perfil financiero ofrece una visión clara y estructurada de la salud financiera del usuario, facilitando la comprensión de sus hábitos financieros y apoyando la toma de decisiones orientadas a mejorar su estabilidad económica.

## Posibles estados

🟢 Saludable
🟡 En observación
🔴 En riesgo

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
    "id": 1,
    "nombre": "Brayan Lira"
  },
  "periodo": {
    "inicio": "2026-07-01",
    "fin": "2026-07-31"
  },
  "ingreso_mensual": 25000,
  "transacciones": [
    {
      "fecha": "2026-07-01",
      "descripcion": "Walmart",
      "monto": 850
    },
    {
      "fecha": "2026-07-02",
      "descripcion": "Pago tarjeta BBVA",
      "monto": 2500
    },
    {
      "fecha": "2026-07-03",
      "descripcion": "CETES",
      "monto": 1000
    },
    {
      "fecha": "2026-07-04",
      "descripcion": "Netflix",
      "monto": 239
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
    "estado": "En observación"
  },
  "dimensiones": {
    "balance_financiero": {
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
      "estado": "En observación",
      "indicadores": {
        "distribucion_gasto_categoria": {
          "Vivienda": 30.2,
          "Alimentación": 21.8,
          "Transporte": 12.5,
          "Salud": 4.8,
          "Educación": 6.5,
          "Entretenimiento": 15.4,
          "Restaurantes": 6.1,
          "Compras personales": 2.7
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
        "Reducir gradualmente el gasto en entretenimiento.",
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







                   

                 

