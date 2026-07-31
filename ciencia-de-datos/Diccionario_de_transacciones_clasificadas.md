# Diccionario de transacciones clasificadas

El siguiente diccionario representa la estructura de datos que sirve como interfaz entre el módulo de Clasificación de Transacciones y el Motor de Análisis Financiero.

Este objeto conserva la estructura del JSON de entrada y enriquece cada transacción con la información generada durante la fase de clasificación mediante inteligencia artificial. A partir de este punto, el motor financiero utiliza únicamente esta información para calcular las variables globales, los indicadores financieros, las puntuaciones y las recomendaciones del usuario.


```python
datos_clasificados = {
    "usuario": {
        "nombre": "Brayan Lira"
    },

    "periodo": {
        "inicio": "2026-07-01",
        "fin": "2026-07-31"
    },

    "ingresos": [
        {
            "fecha": "2026-07-01",
            "descripcion": "Salario",
            "monto": 25000
        },
        {
            "fecha": "2026-07-15",
            "descripcion": "Proyecto freelance",
            "monto": 4500
        }
    ],

    "transacciones": [

        {
            "fecha": "2026-07-02",
            "descripcion": "Walmart León",
            "monto": 1350,
            "forma_pago": "Tarjeta de débito",

            "clasificacion": [
                "Consumo"
            ],

            "categoria": "Alimentación",
            "grupo": "Esencial"
        },

        {
            "fecha": "2026-07-05",
            "descripcion": "Pago préstamo personal",
            "monto": 3200,
            "forma_pago": "Transferencia bancaria",

            "clasificacion": [
                "Pago de deuda"
            ]
        },

        {
            "fecha": "2026-07-10",
            "descripcion": "Aportación fondo de inversión",
            "monto": 2500,
            "forma_pago": "Transferencia bancaria",

            "clasificacion": [
                "Ahorro e inversión"
            ]
        },

        {
            "fecha": "2026-07-15",
            "descripcion": "Liverpool",
            "monto": 4200,
            "forma_pago": "Tarjeta de crédito",
            "tasa_de_interes_de_la_tarjeta": 52.3,

            "clasificacion": [
                "Consumo",
                "Pago de deuda"
            ],

            "categoria": "Compras personales",
            "grupo": "Discrecional"
        },

        {
            "fecha": "2026-07-18",
            "descripcion": "Aportación extraordinaria a inversión",
            "monto": 3000,
            "forma_pago": "Transferencia bancaria",

            "clasificacion": [
                "Ahorro e inversión"
            ]
        }
    ]
}
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
