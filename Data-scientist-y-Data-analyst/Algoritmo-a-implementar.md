# Etapa 1. Recepción de datos

Entrada:
- Recibir el JSON.
- Verificar que tenga la estructura esperada (aunque la validación principal la haga en otra etapa).

Salida:
- Un objeto interno (diccionario o clase) con la información del usuario.

# Etapa 2. Clasificación de transacciones

Para cada transacción:

1. Clasificar el tipo financiero:
- Consumo
- Pago de deuda
- Ahorro e inversión
2. Si es de consumo:
- Clasificar la categoría:
  - Vivienda
  - Alimentación
  - Transporte
  - Salud
  - Educación
  - Entretenimiento
  - Restaurantes
  - Compras personales
  - Viajes
  - Otros
3. A partir de la categoría:
- Asignar el grupo:
  - Esencial
  - Discrecional

Al finalizar esta etapa todas las transacciones ya estarán listas para trabajar.

# Etapa 3. Cálculo de variables derivadas

Se obtienen las variables que utilizarán todas las dimensiones.

Por ejemplo:

- Consumo total
- Pago total de deuda
- Ahorro e inversión total
- Gasto por categoría
- Distribución porcentual
- Egreso total
- Balance mensual
  
# Etapa 4. Evaluación de las dimensiones

- Balance Financiero
  - Calcula sus indicadores.
  - Calcula su estado.
  - Genera sus recomendaciones.

- Capacidad de Ahorro
  - Calcula sus indicadores.
  - Calcula su estado.
  - Genera sus recomendaciones.

- Endeudamiento
  - Calcula sus indicadores.
  - Calcula su estado.
  - Genera sus recomendaciones.

- Comportamiento de Consumo
  - Calcula sus indicadores financieros.
  - Genera el perfil de consumo.
  - Calcula el estado.
  - Genera sus recomendaciones.

# Etapa 5. Construcción del perfil financiero

- Se calcula:
  - Perfil financiero general.
  - Recomendaciones generales.

# Etapa 6. Construcción de la respuesta

- Se crea el JSON con toda la información obtenida.

