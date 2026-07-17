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
- Saludable
- En observación
- En riesgo

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

### ¿Qué preguntas debe responder?
### Variables necesarias
### Indicadores generados
### Resultados posibles de acuerdo a los indicadores

# Ejemplo de ficha de datos de entrada

# Ejemplo de ficha de datos de salida

# Categirias a implementar para clasificar las transacciones

                   

                 

