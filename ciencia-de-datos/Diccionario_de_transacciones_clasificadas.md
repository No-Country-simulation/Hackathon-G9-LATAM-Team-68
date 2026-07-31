# Diccionario de transacciones clasificadas

El siguiente diccionario representa la estructura de datos que sirve como interfaz entre el módulo de Clasificación de Transacciones y el Motor de Análisis Financiero.

Este objeto conserva la estructura del JSON de entrada y enriquece cada transacción con la información generada durante la fase de clasificación mediante inteligencia artificial. A partir de este punto, el motor financiero utiliza únicamente esta información para calcular las variables globales, los indicadores financieros, las puntuaciones y las recomendaciones del usuario.

 ```

```

## Posibles clasificaciones representadas

|Clasificación|	Ejemplo incluido|
| -- | -- |
|Consumo|	Walmart León|
|Pago de deuda|	Pago préstamo personal|
|Ahorro e inversión|	Aportación fondo de inversión|
|Consumo + Pago de deuda|	Compra en Liverpool con tarjeta de crédito|

Como puede observarse, únicamente las transacciones cuya clasificación incluye Consumo contienen adicionalmente los campos categoria y grupo, ya que estos atributos únicamente son aplicables a los gastos de consumo.

Asimismo, cuando la forma de pago corresponde a Tarjeta de crédito, la transacción incorpora el campo tasa_de_interes_de_la_tarjeta, el cual será utilizado posteriormente por el motor de análisis financiero para calcular el indicador Costo promedio del endeudamiento.
