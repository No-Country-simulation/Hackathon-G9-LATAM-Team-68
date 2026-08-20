import joblib
from pathlib import Path
from uuid import UUID
import json
import pandas as pd


# Directorio donde están almacenados los modelos
DIRECTORIO_MODELOS = Path(__file__).resolve().parent / "modelos"


# Carga de los pipelines
pipeline_movimiento = joblib.load(
    DIRECTORIO_MODELOS / "pipeline_tipo_movimiento.joblib"
)

pipeline_categoria = joblib.load(
    DIRECTORIO_MODELOS / "pipeline_categoria.joblib"
)

def validar_json_entrada(datos_entrada):
    """Valida el contrato recibido desde la API."""
    if not isinstance(datos_entrada, dict):
        raise TypeError("El JSON de entrada debe ser un diccionario.")

    if set(datos_entrada) != {
        "usuario", "periodo", "ingresos", "transacciones"
    }:
        raise ValueError(
            "La raíz debe contener usuario, periodo, ingresos y transacciones."
        )

    usuario = datos_entrada["usuario"]
    periodo = datos_entrada["periodo"]
    ingresos = datos_entrada["ingresos"]
    transacciones = datos_entrada["transacciones"]

    if not isinstance(usuario, dict) or set(usuario) != {"id", "nombre"}:
        raise ValueError("usuario debe contener únicamente id y nombre.")

    convertir_uuid(usuario["id"])

    if not isinstance(usuario["nombre"], str) or not usuario["nombre"].strip():
        raise ValueError("usuario.nombre no puede estar vacío.")

    if not isinstance(periodo, dict) or set(periodo) != {"inicio", "fin"}:
        raise ValueError("periodo debe contener únicamente inicio y fin.")

    inicio = convertir_fecha_iso(periodo["inicio"])
    fin = convertir_fecha_iso(periodo["fin"])

    if inicio > fin:
        raise ValueError("periodo.inicio no puede ser posterior a periodo.fin.")

    if not isinstance(ingresos, list):
        raise TypeError("ingresos debe ser una lista.")

    if not isinstance(transacciones, list):
        raise TypeError("transacciones debe ser una lista.")

    for indice, ingreso in enumerate(ingresos):
        if not isinstance(ingreso, dict) or set(ingreso) != {
            "fecha", "descripcion", "monto"
        }:
            raise ValueError(
                f"ingresos[{indice}] debe contener fecha, descripcion y monto."
            )

        fecha = convertir_fecha_iso(ingreso["fecha"])
        if not inicio <= fecha <= fin:
            raise ValueError(f"ingresos[{indice}].fecha está fuera del periodo.")

        if not isinstance(ingreso["descripcion"], str) or not ingreso["descripcion"].strip():
            raise ValueError(f"ingresos[{indice}].descripcion no puede estar vacía.")

        convertir_monto(ingreso["monto"])

    campos_base = {"fecha", "descripcion", "monto", "forma_pago"}
    campo_tasa = "tasa_de_interes_de_la_tarjeta"

    for indice, transaccion in enumerate(transacciones):
        if not isinstance(transaccion, dict):
            raise TypeError(f"transacciones[{indice}] debe ser un diccionario.")

        campos_permitidos = campos_base | {campo_tasa}
        if not campos_base.issubset(transaccion):
            raise ValueError(f"Faltan campos en transacciones[{indice}].")
        if set(transaccion) - campos_permitidos:
            raise ValueError(f"Hay campos desconocidos en transacciones[{indice}].")

        fecha = convertir_fecha_iso(transaccion["fecha"])
        if not inicio <= fecha <= fin:
            raise ValueError(f"transacciones[{indice}].fecha está fuera del periodo.")

        if not isinstance(transaccion["descripcion"], str) or not transaccion["descripcion"].strip():
            raise ValueError(f"transacciones[{indice}].descripcion no puede estar vacía.")

        convertir_monto(transaccion["monto"])

        forma_pago = transaccion["forma_pago"]
        if not isinstance(forma_pago, str) or not forma_pago.strip():
            raise ValueError(f"transacciones[{indice}].forma_pago no puede estar vacía.")

        es_credito = forma_pago == "Tarjeta de crédito"
        tiene_tasa = campo_tasa in transaccion

        if es_credito != tiene_tasa:
            raise ValueError(
                f"transacciones[{indice}] debe incluir la tasa únicamente "
                "cuando utiliza Tarjeta de crédito."
            )

        if tiene_tasa:
            convertir_monto(transaccion[campo_tasa])

    json.dumps(
        datos_entrada,
        ensure_ascii=False,
        allow_nan=False
    )

    return True

def convertir_json_entrada_a_dataframe(datos_entrada):
    """Convierte las transacciones del JSON validado a un DataFrame."""
    usuario = datos_entrada["usuario"]
    periodo = datos_entrada["periodo"]

    columnas = [
        "user_id",
        "nombre",
        "periodo_inicio",
        "periodo_fin",
        "fecha",
        "descripcion",
        "monto",
        "tipo_pago",
        "tasa_de_interes_de_la_tarjeta"
    ]

    filas = []

    for transaccion in datos_entrada["transacciones"]:
        filas.append({
            "user_id": convertir_uuid(usuario["id"]),
            "nombre": usuario["nombre"].strip(),
            "periodo_inicio": periodo["inicio"],
            "periodo_fin": periodo["fin"],
            "fecha": transaccion["fecha"],
            "descripcion": transaccion["descripcion"],
            "monto": transaccion["monto"],
            "tipo_pago": transaccion["forma_pago"],
            "tasa_de_interes_de_la_tarjeta": transaccion.get(
                "tasa_de_interes_de_la_tarjeta"
            )
        })

    return pd.DataFrame(filas, columns=columnas)

def clasificar_usuario(
    datos_usuario,
    datos_entrada,
    pipeline_movimiento,
    pipeline_categoria
):
    columnas_requeridas = {
        "user_id",
        "nombre",
        "periodo_inicio",
        "periodo_fin",
        "fecha",
        "descripcion",
        "monto",
        "tipo_pago",
        "tasa_de_interes_de_la_tarjeta"
    }

    columnas_faltantes = columnas_requeridas.difference(datos_usuario.columns)
    if columnas_faltantes:
        raise ValueError(f"Faltan columnas: {sorted(columnas_faltantes)}")

    datos = datos_usuario.copy().reset_index(drop=True)
    datos["_orden_original"] = range(len(datos))

    if not datos.empty:
        datos["fecha"] = pd.to_datetime(
            datos["fecha"],
            format="%Y-%m-%d",
            errors="raise"
        )
        datos = datos.sort_values(["fecha", "_orden_original"], kind="stable")

    usuario = datos_entrada["usuario"]
    periodo = datos_entrada["periodo"]
    usuario_id = convertir_uuid(usuario["id"])
    nombre = usuario["nombre"].strip()
    periodo_inicio = convertir_fecha_iso(periodo["inicio"])
    periodo_fin = convertir_fecha_iso(periodo["fin"])

    ingresos = [
        {
            "fecha": convertir_fecha_iso(ingreso["fecha"]),
            "descripcion": ingreso["descripcion"].strip(),
            "monto": convertir_monto(ingreso["monto"])
        }
        for ingreso in datos_entrada["ingresos"]
    ]

    if datos.empty:
        predicciones_movimiento = []
        categoria_por_indice = {}
    else:
        textos = datos["descripcion"].astype(str).tolist()
        predicciones_movimiento = pipeline_movimiento.predict(textos)

        indices_consumo = [
            indice
            for indice, movimiento in enumerate(predicciones_movimiento)
            if str(movimiento) == "Consumo"
        ]

        if indices_consumo:
            categorias_consumo = pipeline_categoria.predict(
                [textos[indice] for indice in indices_consumo]
            )
        else:
            categorias_consumo = []

        categoria_por_indice = {
            indice: str(categoria)
            for indice, categoria in zip(indices_consumo, categorias_consumo)
        }

    transacciones = []

    for posicion, ((_, fila), movimiento) in enumerate(
        zip(datos.iterrows(), predicciones_movimiento)
    ):
        movimiento = str(movimiento)

        datos_base = {
            "fecha": convertir_fecha_iso(fila["fecha"]),
            "descripcion": str(fila["descripcion"]).strip(),
            "monto": convertir_monto(fila["monto"])
        }

        # Si una entrada fue colocada por error en transacciones y el modelo
        # la reconoce como ingreso, se integra a la lista de ingresos.
        if movimiento == "Ingreso":
            ingresos.append(datos_base)
            continue

        if movimiento not in CLASIFICACIONES_VALIDAS:
            raise ValueError(f"Clasificación desconocida: {movimiento}")

        forma_pago = str(fila["tipo_pago"])
        transaccion = {**datos_base, "forma_pago": forma_pago}

        if forma_pago == "Tarjeta de crédito":
            tasa = fila["tasa_de_interes_de_la_tarjeta"]
            if pd.isna(tasa):
                raise ValueError(
                    "Una operación con tarjeta de crédito debe incluir su tasa de interés."
                )
            transaccion["tasa_de_interes_de_la_tarjeta"] = round(float(tasa), 2)

        if movimiento == "Consumo":
            categoria = categoria_por_indice[posicion]
            if categoria not in GRUPO_POR_CATEGORIA:
                raise ValueError(f"Categoría desconocida: {categoria}")

            transaccion["clasificacion"] = (
                ["Consumo", "Pago de deuda"]
                if forma_pago == "Tarjeta de crédito"
                else ["Consumo"]
            )
            transaccion["categoria"] = categoria
            transaccion["grupo"] = GRUPO_POR_CATEGORIA[categoria]
        else:
            transaccion["clasificacion"] = [movimiento]

        transacciones.append(transaccion)

    ingresos.sort(key=lambda elemento: elemento["fecha"])

    return {
        "usuario": {
            "id": usuario_id,
            "nombre": nombre
        },
        "periodo": {
            "inicio": periodo_inicio,
            "fin": periodo_fin
        },
        "ingresos": ingresos,
        "transacciones": transacciones
    }

def validar_contrato_json(datos_clasificados):
    """Valida el diccionario producido para el motor financiero."""
    if set(datos_clasificados) != {
        "usuario", "periodo", "ingresos", "transacciones"
    }:
        raise ValueError("La raíz del JSON clasificado no cumple el contrato.")

    if set(datos_clasificados["usuario"]) != {"id", "nombre"}:
        raise ValueError("usuario debe contener id y nombre.")

    convertir_uuid(datos_clasificados["usuario"]["id"])

    if set(datos_clasificados["periodo"]) != {"inicio", "fin"}:
        raise ValueError("periodo debe contener inicio y fin.")

    for ingreso in datos_clasificados["ingresos"]:
        if set(ingreso) != {"fecha", "descripcion", "monto"}:
            raise ValueError("Un ingreso no cumple el contrato.")

    campos_base = {
        "fecha", "descripcion", "monto", "forma_pago", "clasificacion"
    }

    for transaccion in datos_clasificados["transacciones"]:
        if not campos_base.issubset(transaccion):
            raise ValueError("Una transacción no contiene todos los campos base.")

        es_consumo = "Consumo" in transaccion["clasificacion"]
        es_credito = transaccion["forma_pago"] == "Tarjeta de crédito"

        if ("categoria" in transaccion) != es_consumo:
            raise ValueError("categoria debe existir únicamente en consumos.")
        if ("grupo" in transaccion) != es_consumo:
            raise ValueError("grupo debe existir únicamente en consumos.")
        if ("tasa_de_interes_de_la_tarjeta" in transaccion) != es_credito:
            raise ValueError("La presencia de la tasa no coincide con la forma de pago.")

        if es_consumo:
            categoria = transaccion["categoria"]
            if transaccion["grupo"] != GRUPO_POR_CATEGORIA[categoria]:
                raise ValueError("El grupo no corresponde a la categoría.")

    json.dumps(
        datos_clasificados,
        ensure_ascii=False,
        allow_nan=False
    )

    return True

def ejecutar_clasificacion(
    datos_entrada,
    pipeline_movimiento,
    pipeline_categoria
):
    """Ejecuta validación, adaptación, clasificación y validación de salida."""
    validar_json_entrada(datos_entrada)

    datos_usuario = convertir_json_entrada_a_dataframe(datos_entrada)

    datos_clasificados = clasificar_usuario(
        datos_usuario=datos_usuario,
        datos_entrada=datos_entrada,
        pipeline_movimiento=pipeline_movimiento,
        pipeline_categoria=pipeline_categoria
    )

    validar_contrato_json(datos_clasificados)

    return datos_clasificados

def convertir_uuid(valor):
    """Valida y normaliza un identificador UUID."""
    try:
        return str(UUID(str(valor)))
    except (ValueError, TypeError, AttributeError) as error:
        raise ValueError(
            "usuario.id debe contener un UUID válido."
        ) from error
    
def convertir_monto(valor):
    """Valida y convierte un monto a un tipo compatible con JSON."""
    monto = float(valor)

    if not pd.notna(monto) or monto <= 0:
        raise ValueError(
            "Todos los montos deben ser finitos y mayores que cero."
        )

    return round(monto, 2)

def convertir_fecha_iso(valor):
    return pd.to_datetime(
        valor,
        format="%Y-%m-%d",
        errors="raise"
    ).strftime("%Y-%m-%d")

CLASIFICACIONES_VALIDAS = {
    "Consumo",
    "Pago de deuda",
    "Ahorro e inversión"
}

GRUPO_POR_CATEGORIA = {
    "Vivienda": "Esencial",
    "Alimentación": "Esencial",
    "Transporte": "Esencial",
    "Salud": "Esencial",
    "Educación": "Esencial",

    "Entretenimiento y ocio": "Discrecional",
    "Suscripciones digitales": "Discrecional",
    "Compras personales": "Discrecional",
    "Viajes y vacaciones": "Discrecional",
    "Otros": "Discrecional"
}

CATEGORIAS_CONSUMO = [
    "Vivienda",
    "Alimentación",
    "Transporte",
    "Salud",
    "Educación",
    "Entretenimiento y ocio",
    "Suscripciones digitales",
    "Compras personales",
    "Viajes y vacaciones",
    "Otros"
]

PESOS_DIMENSIONES = {

    "balance_financiero": {

        "tasa_de_gasto": 0.50,

        "margen_financiero": 0.50

    },

    "capacidad_de_ahorro": {

        "tasa_de_ahorro": 0.60,

        "aprovechamiento_del_margen_financiero": 0.40

    },

    "endeudamiento": {

        "ratio_de_endeudamiento": 0.40,

        "presion_de_la_deuda": 0.40,

        "costo_promedio_del_endeudamiento": 0.20

    },

    "comportamiento_de_consumo": {

        "indice_de_concentracion_del_gasto": 0.40,

        "predominio_del_gasto": 0.35,

        "diversificacion_del_consumo": 0.25

    }

}

PESOS_PERFIL_FINANCIERO = {

    "balance_financiero": 0.30,

    "capacidad_de_ahorro": 0.25,

    "endeudamiento": 0.25,

    "comportamiento_de_consumo": 0.20

}

MAPA_CATEGORIAS_API = {

    "Vivienda":
        "vivienda",

    "Alimentación":
        "alimentacion",

    "Transporte":
        "transporte",

    "Salud":
        "salud",

    "Educación":
        "educacion",

    "Entretenimiento y ocio":
        "entretenimiento_y_ocio",

    "Suscripciones digitales":
        "suscripciones_digitales",

    "Compras personales":
        "compras_personales",

    "Viajes y vacaciones":
        "viajes_y_vacaciones",

    "Otros":
        "otros"

}

def obtener_estado(puntuacion):

    if puntuacion >= 80:
        return "Saludable"

    elif puntuacion >= 50:
        return "En observación"

    else:
        return "En riesgo"
    
def calcular_ingreso_mensual(datos_clasificados):
    """
    Calcula el ingreso mensual del usuario.

    Parámetros:
        datos_clasificados (dict): Diccionario con la información del usuario.

    Retorna:
        float: Suma de todos los ingresos registrados durante el periodo.
    """

    ingreso_mensual = 0.0

    for ingreso in datos_clasificados["ingresos"]:
        ingreso_mensual += ingreso["monto"]

    return ingreso_mensual

def calcular_consumo_total_mensual(datos_clasificados):
    """
    Calcula el consumo total mensual del usuario.

    Se consideran únicamente las transacciones cuya clasificación
    contenga exclusivamente la etiqueta "Consumo".

    Parámetros:
        datos_clasificados (dict): Diccionario con las transacciones clasificadas.

    Retorna:
        float: Consumo total mensual.
    """

    consumo_total_mensual = 0.0

    for transaccion in datos_clasificados["transacciones"]:

        clasificacion = transaccion["clasificacion"]

        if (
            "Consumo" in clasificacion
            and len(clasificacion) == 1
        ):
            consumo_total_mensual += transaccion["monto"]

    return consumo_total_mensual

def calcular_pago_mensual_de_deudas(datos_clasificados):
    """
    Calcula el pago mensual de deudas del usuario.

    Se consideran todas las transacciones cuya clasificación
    incluya la etiqueta "Pago de deuda", independientemente
    de si también pertenecen a otra clasificación.

    Parámetros:
        datos_clasificados (dict): Diccionario con las transacciones clasificadas.

    Retorna:
        float: Pago mensual de deudas.
    """

    pago_mensual_de_deudas = 0.0

    for transaccion in datos_clasificados["transacciones"]:

        clasificacion = transaccion["clasificacion"]

        if "Pago de deuda" in clasificacion:
            pago_mensual_de_deudas += transaccion["monto"]

    return pago_mensual_de_deudas

def calcular_ahorro_e_inversion_total(datos_clasificados):
    """
    Calcula el ahorro e inversión total del usuario.

    Se consideran todas las transacciones cuya clasificación
    incluya la etiqueta "Ahorro e inversión".

    Parámetros:
        datos_clasificados (dict): Diccionario con las transacciones clasificadas.

    Retorna:
        float: Ahorro e inversión total.
    """

    ahorro_e_inversion_total = 0.0

    for transaccion in datos_clasificados["transacciones"]:

        clasificacion = transaccion["clasificacion"]

        if "Ahorro e inversión" in clasificacion:
            ahorro_e_inversion_total += transaccion["monto"]

    return ahorro_e_inversion_total

def calcular_egreso_total(consumo_total_mensual, pago_mensual_de_deudas):
    """
    Calcula el egreso total del usuario.

    El egreso total corresponde a la suma del consumo total mensual
    y el pago mensual de deudas.

    Parámetros:
        consumo_total_mensual (float): Consumo total mensual del usuario.
        pago_mensual_de_deudas (float): Pago mensual de deudas del usuario.

    Retorna:
        float: Egreso total del usuario.
    """

    egreso_total = consumo_total_mensual + pago_mensual_de_deudas

    return egreso_total

def calcular_balance_mensual(ingreso_mensual, egreso_total):
    """
    Calcula el balance mensual del usuario.

    El balance mensual corresponde a la diferencia entre el ingreso
    mensual y el egreso total del periodo.

    Parámetros:
        ingreso_mensual (float): Ingreso mensual del usuario.
        egreso_total (float): Egreso total del usuario.

    Retorna:
        float: Balance mensual del usuario.
    """

    balance_mensual = ingreso_mensual - egreso_total

    return balance_mensual

def calcular_consumo_total_por_categoria(datos_clasificados):
    """
    Calcula el consumo total por categoría del usuario.

    Se consideran todas las transacciones cuya clasificación
    incluya la etiqueta "Consumo", independientemente de que
    también estén clasificadas como "Pago de deuda".

    Parámetros:
        datos_clasificados (dict): Diccionario con las transacciones clasificadas.

    Retorna:
        float: Consumo total por categoría.
    """

    consumo_total_por_categoria = 0.0

    for transaccion in datos_clasificados["transacciones"]:

        clasificacion = transaccion["clasificacion"]

        if "Consumo" in clasificacion:
            consumo_total_por_categoria += transaccion["monto"]

    return consumo_total_por_categoria

def calcular_gasto_por_categoria(datos_clasificados):
    """
    Calcula el gasto acumulado por categoría de consumo.

    Se consideran todas las transacciones cuya clasificación
    incluya la etiqueta "Consumo", independientemente de que
    también estén clasificadas como "Pago de deuda".

    Parámetros:
        datos_clasificados (dict): Diccionario con las transacciones clasificadas.

    Retorna:
        dict: Diccionario con el gasto acumulado por cada categoría.
    """

    # Inicializar todas las categorías en 0.0
    gasto_por_categoria = {
        categoria: 0.0
        for categoria in CATEGORIAS_CONSUMO
    }

    # Recorrer las transacciones
    for transaccion in datos_clasificados["transacciones"]:

        clasificacion = transaccion["clasificacion"]

        if "Consumo" in clasificacion:

            categoria = transaccion["categoria"]

            gasto_por_categoria[categoria] += transaccion["monto"]

    return gasto_por_categoria

def calcular_distribucion_porcentual_gasto(
    gasto_por_categoria,
    consumo_total_por_categoria
):
    """
    Calcula la distribución porcentual del gasto por categoría.

    La distribución porcentual representa el porcentaje que ocupa
    cada categoría respecto al consumo total por categoría.

    Parámetros:
        gasto_por_categoria (dict): Gasto acumulado por categoría.
        consumo_total_por_categoria (float): Consumo total por categoría.

    Retorna:
        dict: Distribución porcentual del gasto por categoría.
    """

    # Inicializar todas las categorías en 0.0
    distribucion_porcentual_gasto = {
        categoria: 0.0
        for categoria in CATEGORIAS_CONSUMO
    }

    # Evitar división entre cero
    if consumo_total_por_categoria == 0.0:
        return distribucion_porcentual_gasto

    # Calcular la distribución porcentual
    for categoria in CATEGORIAS_CONSUMO:

        distribucion_porcentual_gasto[categoria] = (
            gasto_por_categoria[categoria]
            / consumo_total_por_categoria
        ) * 100

    return distribucion_porcentual_gasto

def calcular_tasa_interes_promedio_ponderada(datos_clasificados):
    """
    Calcula la tasa de interés promedio ponderada de las compras
    realizadas con tarjeta de crédito.

    El promedio se calcula utilizando el monto de cada transacción
    como peso.

    Parámetros:
        datos_clasificados (dict): Diccionario con las transacciones clasificadas.

    Retorna:
        float: Tasa de interés promedio ponderada.
    """

    monto_total_credito = 0.0
    suma_ponderada = 0.0

    # Recorrer las transacciones
    for transaccion in datos_clasificados["transacciones"]:

        if transaccion["forma_pago"] == "Tarjeta de crédito":

            monto = transaccion["monto"]
            tasa = transaccion["tasa_de_interes_de_la_tarjeta"]

            monto_total_credito += monto
            suma_ponderada += monto * tasa

    # Evitar división entre cero
    if monto_total_credito == 0.0:
        return 0.0

    tasa_interes_promedio_ponderada = (
        suma_ponderada / monto_total_credito
    )

    return tasa_interes_promedio_ponderada

def calcular_variables_globales(datos_clasificados):
    """
    Calcula todas las variables globales necesarias para el
    motor de análisis financiero.

    Parámetros:
        datos_clasificados (dict): Diccionario con las transacciones clasificadas.

    Retorna:
        dict: Diccionario con todas las variables globales.
    """

    # Variables obtenidas directamente del diccionario
    ingreso_mensual = calcular_ingreso_mensual(datos_clasificados)

    consumo_total_mensual = calcular_consumo_total_mensual(
        datos_clasificados
    )

    pago_mensual_de_deudas = calcular_pago_mensual_de_deudas(
        datos_clasificados
    )

    ahorro_e_inversion_total = calcular_ahorro_e_inversion_total(
        datos_clasificados
    )

    consumo_total_por_categoria = calcular_consumo_total_por_categoria(
        datos_clasificados
    )

    gasto_por_categoria = calcular_gasto_por_categoria(
        datos_clasificados
    )

    tasa_interes_promedio_ponderada = (
        calcular_tasa_interes_promedio_ponderada(
            datos_clasificados
        )
    )

    # Variables derivadas
    egreso_total = calcular_egreso_total(
        consumo_total_mensual,
        pago_mensual_de_deudas
    )

    balance_mensual = calcular_balance_mensual(
        ingreso_mensual,
        egreso_total
    )

    distribucion_porcentual_gasto = (
        calcular_distribucion_porcentual_gasto(
            gasto_por_categoria,
            consumo_total_por_categoria
        )
    )

    # Construcción del diccionario de salida
    variables_globales = {

        "ingreso_mensual": ingreso_mensual,

        "consumo_total_mensual": consumo_total_mensual,

        "pago_mensual_de_deudas": pago_mensual_de_deudas,

        "ahorro_e_inversion_total": ahorro_e_inversion_total,

        "egreso_total": egreso_total,

        "balance_mensual": balance_mensual,

        "consumo_total_por_categoria": consumo_total_por_categoria,

        "gasto_por_categoria": gasto_por_categoria,

        "distribucion_porcentual_gasto": (
            distribucion_porcentual_gasto
        ),

        "tasa_interes_promedio_ponderada": (
            tasa_interes_promedio_ponderada
        )
    }

    return variables_globales

def calcular_indicadores_balance_financiero(variables_globales):
    """
    Calcula los indicadores de la dimensión Balance Financiero.

    Parámetros:
        variables_globales (dict): Diccionario con las variables
        globales calculadas previamente.

    Retorna:
        dict: Diccionario con los indicadores de la dimensión
        Balance Financiero.
    """

    ingreso_mensual = variables_globales["ingreso_mensual"]
    egreso_total = variables_globales["egreso_total"]
    balance_mensual = variables_globales["balance_mensual"]

    # Indicador 1: Balance mensual
    indicador_balance_mensual = balance_mensual

    # Indicador 2: Tasa de gasto
    if ingreso_mensual == 0.0:
        indicador_tasa_de_gasto = 0.0
    else:
        indicador_tasa_de_gasto = (
            egreso_total / ingreso_mensual
        )

    # Indicador 3: Margen financiero
    if ingreso_mensual == 0.0:
        indicador_margen_financiero = 0.0
    else:
        indicador_margen_financiero = (
            balance_mensual / ingreso_mensual
        )

    indicadores_balance_financiero = {

        "balance_mensual": indicador_balance_mensual,

        "tasa_de_gasto": indicador_tasa_de_gasto,

        "margen_financiero": indicador_margen_financiero

    }

    return indicadores_balance_financiero

def calcular_indicadores_capacidad_ahorro(variables_globales):
    """
    Calcula los indicadores de la dimensión Capacidad de Ahorro.

    Parámetros:
        variables_globales (dict): Diccionario con las variables
        globales calculadas previamente.

    Retorna:
        dict: Diccionario con los indicadores de la dimensión
        Capacidad de Ahorro.
    """

    ingreso_mensual = variables_globales["ingreso_mensual"]
    ahorro_e_inversion_total = variables_globales["ahorro_e_inversion_total"]
    balance_mensual = variables_globales["balance_mensual"]

    # Indicador 1: Tasa de ahorro
    if ingreso_mensual == 0.0:
        indicador_tasa_de_ahorro = 0.0
    else:
        indicador_tasa_de_ahorro = (
            ahorro_e_inversion_total / ingreso_mensual
        )

    # Indicador 2: Ahorro e inversión del periodo
    indicador_ahorro_e_inversion_del_periodo = (
        ahorro_e_inversion_total
    )

    # Indicador 3: Aprovechamiento del margen financiero
    if balance_mensual <= 0.0:
        indicador_aprovechamiento_del_margen_financiero = 0.0
    else:
        indicador_aprovechamiento_del_margen_financiero = (
            ahorro_e_inversion_total / balance_mensual
        )

    indicadores_capacidad_ahorro = {

        "tasa_de_ahorro": indicador_tasa_de_ahorro,

        "ahorro_e_inversion_del_periodo":
            indicador_ahorro_e_inversion_del_periodo,

        "aprovechamiento_del_margen_financiero":
            indicador_aprovechamiento_del_margen_financiero

    }

    return indicadores_capacidad_ahorro

def calcular_indicadores_endeudamiento(variables_globales):
    """
    Calcula los indicadores de la dimensión Endeudamiento.

    Parámetros:
        variables_globales (dict): Diccionario con las variables
        globales calculadas previamente.

    Retorna:
        dict: Diccionario con los indicadores de la dimensión
        Endeudamiento.
    """

    ingreso_mensual = variables_globales["ingreso_mensual"]
    pago_mensual_de_deudas = variables_globales["pago_mensual_de_deudas"]
    egreso_total = variables_globales["egreso_total"]
    tasa_interes_promedio_ponderada = (
        variables_globales["tasa_interes_promedio_ponderada"]
    )

    # Indicador 1: Ratio de endeudamiento
    if ingreso_mensual == 0.0:
        indicador_ratio_de_endeudamiento = 0.0
    else:
        indicador_ratio_de_endeudamiento = (
            pago_mensual_de_deudas / ingreso_mensual
        )

    # Indicador 2: Monto destinado al pago de deudas
    indicador_monto_destinado_al_pago_de_deudas = (
        pago_mensual_de_deudas
    )

    # Indicador 3: Presión de la deuda
    if egreso_total == 0.0:
        indicador_presion_de_la_deuda = 0.0
    else:
        indicador_presion_de_la_deuda = (
            pago_mensual_de_deudas / egreso_total
        )

    # Indicador 4: Costo promedio del endeudamiento
    indicador_costo_promedio_del_endeudamiento = (
        tasa_interes_promedio_ponderada
    )

    indicadores_endeudamiento = {

        "ratio_de_endeudamiento":
            indicador_ratio_de_endeudamiento,

        "monto_destinado_al_pago_de_deudas":
            indicador_monto_destinado_al_pago_de_deudas,

        "presion_de_la_deuda":
            indicador_presion_de_la_deuda,

        "costo_promedio_del_endeudamiento":
            indicador_costo_promedio_del_endeudamiento

    }

    return indicadores_endeudamiento

def calcular_indicadores_comportamiento_consumo(
    variables_globales,
    datos_clasificados
):
    """
    Calcula los indicadores de la dimensión Comportamiento de Consumo.

    Parámetros:
        variables_globales (dict): Diccionario con las variables
        globales calculadas previamente.
        datos_clasificados (dict): Diccionario con las transacciones
        clasificadas.

    Retorna:
        dict: Diccionario con los indicadores de la dimensión
        Comportamiento de Consumo.
    """

    distribucion_porcentual_gasto = (
        variables_globales["distribucion_porcentual_gasto"]
    )

    consumo_total_por_categoria = (
        variables_globales["consumo_total_por_categoria"]
    )

    gasto_por_categoria = (
        variables_globales["gasto_por_categoria"]
    )

    # ==========================================================
    # Indicador 1: Distribución del gasto por categoría
    # ==========================================================

    indicador_distribucion_del_gasto_por_categoria = (
        distribucion_porcentual_gasto
    )

    # ==========================================================
    # Indicador 2: Índice de concentración del gasto
    # (HHI normalizado)
    # ==========================================================

    if consumo_total_por_categoria == 0.0:

        indicador_indice_de_concentracion_del_gasto = 0.0

    else:

        hhi = 0.0

        for porcentaje in distribucion_porcentual_gasto.values():

            proporcion = porcentaje / 100

            hhi += proporcion ** 2

        n = len(CATEGORIAS_CONSUMO)

        indicador_indice_de_concentracion_del_gasto = (
            (hhi - (1 / n))
            /
            (1 - (1 / n))
        )

    # ==========================================================
    # Perfil de consumo
    # ==========================================================

    # ----------------------------------------------------------
    # Indicador de consumo 1: Predominio del gasto
    # ----------------------------------------------------------

    gasto_esencial = 0.0
    gasto_discrecional = 0.0

    for transaccion in datos_clasificados["transacciones"]:

        if "Consumo" in transaccion["clasificacion"]:

            if transaccion["grupo"] == "Esencial":

                gasto_esencial += transaccion["monto"]

            elif transaccion["grupo"] == "Discrecional":

                gasto_discrecional += transaccion["monto"]

    if consumo_total_por_categoria == 0.0:

        indicador_predominio_del_gasto = (
            "Balance entre gastos esenciales y discrecionales"
        )

    else:

        porcentaje_esencial = (
            gasto_esencial / consumo_total_por_categoria
        )

        porcentaje_discrecional = (
            gasto_discrecional / consumo_total_por_categoria
        )

        if porcentaje_esencial >= 0.60:

            indicador_predominio_del_gasto = (
                "Predominio en gastos esenciales"
            )

        elif porcentaje_discrecional >= 0.60:

            indicador_predominio_del_gasto = (
                "Predominio en gastos discrecionales"
            )

        else:

            indicador_predominio_del_gasto = (
                "Balance entre gastos esenciales y discrecionales"
            )

    # ----------------------------------------------------------
    # Indicador de consumo 2: Tipo de consumo
    # ----------------------------------------------------------

    indice = indicador_indice_de_concentracion_del_gasto

    if indice <= 0.33:

        indicador_tipo_de_consumo = (
            "Consumo equilibrado"
        )

    elif indice <= 0.66:

        indicador_tipo_de_consumo = (
            "Consumo moderadamente concentrado"
        )

    else:

        indicador_tipo_de_consumo = (
            "Consumo altamente concentrado"
        )

    # ----------------------------------------------------------
    # Indicador de consumo 3: Diversificación del consumo
    # ----------------------------------------------------------

    categorias_utilizadas = 0

    for monto in gasto_por_categoria.values():

        if monto > 0:

            categorias_utilizadas += 1

    if categorias_utilizadas >= 5:

        indicador_diversificacion_del_consumo = (
            "Consumo diversificado"
        )

    else:

        indicador_diversificacion_del_consumo = (
            "Consumo poco diversificado"
        )

    # ----------------------------------------------------------
    # Indicador de consumo 4: Categoría predominante
    # ----------------------------------------------------------

    if consumo_total_por_categoria == 0.0:

        indicador_categoria_predominante = "Ninguna"

    else:

        indicador_categoria_predominante = max(
            distribucion_porcentual_gasto,
            key=distribucion_porcentual_gasto.get
        )

    indicadores_comportamiento_consumo = {

        "distribucion_del_gasto_por_categoria":
            indicador_distribucion_del_gasto_por_categoria,

        "indice_de_concentracion_del_gasto":
            indicador_indice_de_concentracion_del_gasto,

        "perfil_de_consumo": {

            "predominio_del_gasto":
                indicador_predominio_del_gasto,

            "tipo_de_consumo":
                indicador_tipo_de_consumo,

            "diversificacion_del_consumo":
                indicador_diversificacion_del_consumo,

            "categoria_predominante":
                indicador_categoria_predominante
        }

    }

    return indicadores_comportamiento_consumo

def calcular_indicadores_financieros(
    variables_globales,
    datos_clasificados
):
    """
    Calcula todos los indicadores financieros del sistema.

    Parámetros:
        variables_globales (dict): Diccionario con las variables
        globales calculadas previamente.
        datos_clasificados (dict): Diccionario con las transacciones
        clasificadas.

    Retorna:
        dict: Diccionario con los indicadores financieros de las
        cuatro dimensiones.
    """

    indicadores_balance_financiero = (
        calcular_indicadores_balance_financiero(
            variables_globales
        )
    )

    indicadores_capacidad_ahorro = (
        calcular_indicadores_capacidad_ahorro(
            variables_globales
        )
    )

    indicadores_endeudamiento = (
        calcular_indicadores_endeudamiento(
            variables_globales
        )
    )

    indicadores_comportamiento_consumo = (
        calcular_indicadores_comportamiento_consumo(
            variables_globales,
            datos_clasificados
        )
    )

    indicadores_financieros = {

        "balance_financiero":
            indicadores_balance_financiero,

        "capacidad_de_ahorro":
            indicadores_capacidad_ahorro,

        "endeudamiento":
            indicadores_endeudamiento,

        "comportamiento_de_consumo":
            indicadores_comportamiento_consumo

    }

    return indicadores_financieros

def evaluar_balance_financiero(indicadores_financieros):
    """
    Evalúa la dimensión Balance Financiero.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

    Retorna:
        dict: Diccionario con la puntuación y estado de la dimensión.
    """

    indicadores = indicadores_financieros["balance_financiero"]

    tasa_de_gasto = indicadores["tasa_de_gasto"]
    margen_financiero = indicadores["margen_financiero"]

    # ==========================================================
    # Puntuación del indicador: Tasa de gasto
    # ==========================================================

    if tasa_de_gasto <= 0.50:
        puntuacion_tasa_de_gasto = 100

    elif tasa_de_gasto <= 0.60:
        puntuacion_tasa_de_gasto = 90

    elif tasa_de_gasto <= 0.70:
        puntuacion_tasa_de_gasto = 80

    elif tasa_de_gasto <= 0.80:
        puntuacion_tasa_de_gasto = 70

    elif tasa_de_gasto <= 0.90:
        puntuacion_tasa_de_gasto = 60

    elif tasa_de_gasto <= 1.00:
        puntuacion_tasa_de_gasto = 50

    else:
        puntuacion_tasa_de_gasto = 0

    # ==========================================================
    # Puntuación del indicador: Margen financiero
    # ==========================================================

    if margen_financiero >= 0.50:
        puntuacion_margen_financiero = 100

    elif margen_financiero >= 0.40:
        puntuacion_margen_financiero = 90

    elif margen_financiero >= 0.30:
        puntuacion_margen_financiero = 80

    elif margen_financiero >= 0.20:
        puntuacion_margen_financiero = 70

    elif margen_financiero >= 0.10:
        puntuacion_margen_financiero = 60

    elif margen_financiero >= 0.00:
        puntuacion_margen_financiero = 50

    else:
        puntuacion_margen_financiero = 0

    # ==========================================================
    # Puntuación de la dimensión
    # ==========================================================

    pesos = PESOS_DIMENSIONES["balance_financiero"]

    puntuacion_dimension = round(

        (puntuacion_tasa_de_gasto *
         pesos["tasa_de_gasto"])

        +

        (puntuacion_margen_financiero *
         pesos["margen_financiero"])

    )

    # ==========================================================
    # Estado de la dimensión
    # ==========================================================

    estado = obtener_estado(puntuacion_dimension)

    evaluacion_balance_financiero = {

        "puntuacion": puntuacion_dimension,

        "estado": estado

    }

    return evaluacion_balance_financiero

def evaluar_capacidad_de_ahorro(indicadores_financieros):
    """
    Evalúa la dimensión Capacidad de Ahorro.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

    Retorna:
        dict: Diccionario con la puntuación y estado de la dimensión.
    """

    indicadores = indicadores_financieros["capacidad_de_ahorro"]

    tasa_de_ahorro = indicadores["tasa_de_ahorro"]

    aprovechamiento_del_margen_financiero = (
        indicadores["aprovechamiento_del_margen_financiero"]
    )

    # ==========================================================
    # Puntuación del indicador: Tasa de ahorro
    # ==========================================================

    if tasa_de_ahorro >= 0.30:
        puntuacion_tasa_de_ahorro = 100

    elif tasa_de_ahorro >= 0.25:
        puntuacion_tasa_de_ahorro = 90

    elif tasa_de_ahorro >= 0.20:
        puntuacion_tasa_de_ahorro = 80

    elif tasa_de_ahorro >= 0.15:
        puntuacion_tasa_de_ahorro = 70

    elif tasa_de_ahorro >= 0.10:
        puntuacion_tasa_de_ahorro = 60

    elif tasa_de_ahorro >= 0.05:
        puntuacion_tasa_de_ahorro = 50

    else:
        puntuacion_tasa_de_ahorro = 0

    # ==========================================================
    # Puntuación del indicador:
    # Aprovechamiento del margen financiero
    # ==========================================================

    if aprovechamiento_del_margen_financiero >= 0.90:
        puntuacion_aprovechamiento = 100

    elif aprovechamiento_del_margen_financiero >= 0.75:
        puntuacion_aprovechamiento = 90

    elif aprovechamiento_del_margen_financiero >= 0.60:
        puntuacion_aprovechamiento = 80

    elif aprovechamiento_del_margen_financiero >= 0.45:
        puntuacion_aprovechamiento = 70

    elif aprovechamiento_del_margen_financiero >= 0.30:
        puntuacion_aprovechamiento = 60

    elif aprovechamiento_del_margen_financiero >= 0.15:
        puntuacion_aprovechamiento = 50

    else:
        puntuacion_aprovechamiento = 0

    # ==========================================================
    # Puntuación de la dimensión
    # ==========================================================

    pesos = PESOS_DIMENSIONES["capacidad_de_ahorro"]

    puntuacion_dimension = round(

        (puntuacion_tasa_de_ahorro *
         pesos["tasa_de_ahorro"])

        +

        (puntuacion_aprovechamiento *
         pesos["aprovechamiento_del_margen_financiero"])

    )

    # ==========================================================
    # Estado de la dimensión
    # ==========================================================

    estado = obtener_estado(puntuacion_dimension)

    evaluacion_capacidad_de_ahorro = {

        "puntuacion": puntuacion_dimension,

        "estado": estado

    }

    return evaluacion_capacidad_de_ahorro

def evaluar_endeudamiento(indicadores_financieros):
    """
    Evalúa la dimensión Endeudamiento.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

    Retorna:
        dict: Diccionario con la puntuación y estado de la dimensión.
    """

    indicadores = indicadores_financieros["endeudamiento"]

    ratio_de_endeudamiento = (
        indicadores["ratio_de_endeudamiento"]
    )

    presion_de_la_deuda = (
        indicadores["presion_de_la_deuda"]
    )

    costo_promedio_del_endeudamiento = (
        indicadores["costo_promedio_del_endeudamiento"]
    )

    # ==========================================================
    # Puntuación del indicador: Ratio de endeudamiento
    # ==========================================================

    if ratio_de_endeudamiento <= 0.10:
        puntuacion_ratio = 100

    elif ratio_de_endeudamiento <= 0.20:
        puntuacion_ratio = 90

    elif ratio_de_endeudamiento <= 0.30:
        puntuacion_ratio = 80

    elif ratio_de_endeudamiento <= 0.40:
        puntuacion_ratio = 70

    elif ratio_de_endeudamiento <= 0.50:
        puntuacion_ratio = 60

    elif ratio_de_endeudamiento <= 0.60:
        puntuacion_ratio = 50

    else:
        puntuacion_ratio = 0

    # ==========================================================
    # Puntuación del indicador: Presión de la deuda
    # ==========================================================

    if presion_de_la_deuda <= 0.10:
        puntuacion_presion = 100

    elif presion_de_la_deuda <= 0.20:
        puntuacion_presion = 90

    elif presion_de_la_deuda <= 0.30:
        puntuacion_presion = 80

    elif presion_de_la_deuda <= 0.40:
        puntuacion_presion = 70

    elif presion_de_la_deuda <= 0.50:
        puntuacion_presion = 60

    elif presion_de_la_deuda <= 0.60:
        puntuacion_presion = 50

    else:
        puntuacion_presion = 0

    # ==========================================================
    # Puntuación del indicador:
    # Costo promedio del endeudamiento
    # ==========================================================

    if costo_promedio_del_endeudamiento <= 10:
        puntuacion_costo = 100

    elif costo_promedio_del_endeudamiento <= 20:
        puntuacion_costo = 90

    elif costo_promedio_del_endeudamiento <= 35:
        puntuacion_costo = 80

    elif costo_promedio_del_endeudamiento <= 50:
        puntuacion_costo = 70

    elif costo_promedio_del_endeudamiento <= 65:
        puntuacion_costo = 60

    elif costo_promedio_del_endeudamiento <= 80:
        puntuacion_costo = 50

    else:
        puntuacion_costo = 0

    # ==========================================================
    # Puntuación de la dimensión
    # ==========================================================

    pesos = PESOS_DIMENSIONES["endeudamiento"]

    puntuacion_dimension = round(

        (puntuacion_ratio *
         pesos["ratio_de_endeudamiento"])

        +

        (puntuacion_presion *
         pesos["presion_de_la_deuda"])

        +

        (puntuacion_costo *
         pesos["costo_promedio_del_endeudamiento"])

    )

    # ==========================================================
    # Estado de la dimensión
    # ==========================================================

    estado = obtener_estado(puntuacion_dimension)

    evaluacion_endeudamiento = {

        "puntuacion": puntuacion_dimension,

        "estado": estado

    }

    return evaluacion_endeudamiento

def evaluar_comportamiento_de_consumo(
    indicadores_financieros,
    variables_globales
):
    """
    Evalúa la dimensión Comportamiento de Consumo.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

        variables_globales (dict): Diccionario con las variables
        globales calculadas previamente.

    Retorna:
        dict: Diccionario con la puntuación y estado de la dimensión.
    """

    consumo_total_por_categoria = (
        variables_globales["consumo_total_por_categoria"]
    )

    # ==========================================================
    # Caso especial:
    # No existen transacciones de consumo
    # ==========================================================

    if consumo_total_por_categoria == 0.0:

        return {

            "puntuacion": 0,

            "estado": obtener_estado(0)

        }

    indicadores = indicadores_financieros["comportamiento_de_consumo"]

    indice_de_concentracion_del_gasto = (
        indicadores["indice_de_concentracion_del_gasto"]
    )

    perfil_de_consumo = indicadores["perfil_de_consumo"]

    predominio_del_gasto = (
        perfil_de_consumo["predominio_del_gasto"]
    )

    diversificacion_del_consumo = (
        perfil_de_consumo["diversificacion_del_consumo"]
    )

    # ==========================================================
    # Puntuación del indicador:
    # Índice de concentración del gasto
    # ==========================================================

    if indice_de_concentracion_del_gasto <= 0.33:

        puntuacion_indice = 100

    elif indice_de_concentracion_del_gasto <= 0.66:

        puntuacion_indice = 70

    else:

        puntuacion_indice = 40

    # ==========================================================
    # Puntuación del indicador:
    # Predominio del gasto
    # ==========================================================

    if predominio_del_gasto == (
        "Predominio en gastos esenciales"
    ):

        puntuacion_predominio = 100

    elif predominio_del_gasto == (
        "Balance entre gastos esenciales y discrecionales"
    ):

        puntuacion_predominio = 80

    else:

        puntuacion_predominio = 50

    # ==========================================================
    # Puntuación del indicador:
    # Diversificación del consumo
    # ==========================================================

    if diversificacion_del_consumo == (
        "Consumo diversificado"
    ):

        puntuacion_diversificacion = 100

    else:

        puntuacion_diversificacion = 50

    # ==========================================================
    # Puntuación de la dimensión
    # ==========================================================

    pesos = PESOS_DIMENSIONES["comportamiento_de_consumo"]

    puntuacion_dimension = round(

        (puntuacion_indice *
         pesos["indice_de_concentracion_del_gasto"])

        +

        (puntuacion_predominio *
         pesos["predominio_del_gasto"])

        +

        (puntuacion_diversificacion *
         pesos["diversificacion_del_consumo"])

    )

    # ==========================================================
    # Estado de la dimensión
    # ==========================================================

    estado = obtener_estado(puntuacion_dimension)

    evaluacion_comportamiento_de_consumo = {

        "puntuacion": puntuacion_dimension,

        "estado": estado

    }

    return evaluacion_comportamiento_de_consumo

def calcular_evaluacion_financiera(
    indicadores_financieros,
    variables_globales
):
    """
    Calcula la evaluación financiera de las cuatro dimensiones.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

        variables_globales (dict): Diccionario con las variables
        globales previamente calculadas.

    Retorna:
        dict: Diccionario con la puntuación y estado de cada dimensión.
    """

    evaluacion_balance_financiero = (
        evaluar_balance_financiero(
            indicadores_financieros
        )
    )

    evaluacion_capacidad_de_ahorro = (
        evaluar_capacidad_de_ahorro(
            indicadores_financieros
        )
    )

    evaluacion_endeudamiento = (
        evaluar_endeudamiento(
            indicadores_financieros
        )
    )

    evaluacion_comportamiento_de_consumo = (
        evaluar_comportamiento_de_consumo(
            indicadores_financieros,
            variables_globales
        )
    )

    evaluacion_financiera = {

        "balance_financiero":
            evaluacion_balance_financiero,

        "capacidad_de_ahorro":
            evaluacion_capacidad_de_ahorro,

        "endeudamiento":
            evaluacion_endeudamiento,

        "comportamiento_de_consumo":
            evaluacion_comportamiento_de_consumo

    }

    return evaluacion_financiera

def generar_recomendaciones_balance_financiero(
    indicadores_financieros,
    evaluacion_financiera
):
    """
    Genera las recomendaciones para la dimensión Balance Financiero.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera previamente calculada.

    Retorna:
        list: Lista de recomendaciones para la dimensión.
    """

    recomendaciones = []

    indicadores = indicadores_financieros["balance_financiero"]

    balance_mensual = indicadores["balance_mensual"]
    tasa_de_gasto = indicadores["tasa_de_gasto"]
    margen_financiero = indicadores["margen_financiero"]

    estado = (
        evaluacion_financiera["balance_financiero"]["estado"]
    )

    # ==========================================================
    # Recomendación según el Balance mensual
    # ==========================================================

    if balance_mensual > 0:

        recomendaciones.append(
            "Mantener un balance mensual positivo para fortalecer la estabilidad financiera."
        )

    elif balance_mensual == 0:

        recomendaciones.append(
            "Buscar generar un balance mensual positivo incrementando los ingresos o reduciendo los gastos."
        )

    else:

        recomendaciones.append(
            "Recuperar un balance mensual positivo reduciendo gastos o incrementando los ingresos."
        )

    # ==========================================================
    # Recomendación según la Tasa de gasto
    # ==========================================================

    if tasa_de_gasto <= 0.50:

        recomendaciones.append(
            "Mantener el nivel actual de gasto respecto a los ingresos."
        )

    elif tasa_de_gasto <= 0.80:

        recomendaciones.append(
            "Continuar monitoreando el gasto para evitar que aumente."
        )

    elif tasa_de_gasto <= 1.00:

        recomendaciones.append(
            "Reducir gradualmente el porcentaje destinado al gasto mensual."
        )

    else:

        recomendaciones.append(
            "Priorizar la reducción inmediata de gastos o incrementar los ingresos para recuperar el equilibrio financiero."
        )

    # ==========================================================
    # Recomendación según el Margen financiero
    # ==========================================================

    if margen_financiero >= 0.30:

        recomendaciones.append(
            "Mantener el margen financiero actual y destinar parte del excedente al ahorro o inversión."
        )

    elif margen_financiero >= 0.10:

        recomendaciones.append(
            "Buscar incrementar gradualmente el margen financiero mediante una mejor planificación del presupuesto."
        )

    elif margen_financiero >= 0.00:

        recomendaciones.append(
            "Incrementar el margen financiero reduciendo gastos no esenciales o aumentando los ingresos."
        )

    else:

        recomendaciones.append(
            "Recuperar un margen financiero positivo disminuyendo gastos o incrementando los ingresos antes de asumir nuevos compromisos financieros."
        )

    # ==========================================================
    # Recomendación según el Estado de la dimensión
    # ==========================================================

    if estado == "Saludable":

        recomendaciones.append(
            "Mantener las prácticas financieras actuales para conservar el buen desempeño de esta dimensión."
        )

    elif estado == "En observación":

        recomendaciones.append(
            "Dar seguimiento mensual a esta dimensión para evitar que evolucione hacia una situación de riesgo."
        )

    else:

        recomendaciones.append(
            "Priorizar la mejora de esta dimensión antes de asumir nuevos compromisos financieros."
        )

    return recomendaciones

def generar_recomendaciones_capacidad_de_ahorro(
    indicadores_financieros,
    evaluacion_financiera
):
    """
    Genera las recomendaciones para la dimensión Capacidad de Ahorro.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera previamente calculada.

    Retorna:
        list: Lista de recomendaciones para la dimensión.
    """

    recomendaciones = []

    indicadores = indicadores_financieros["capacidad_de_ahorro"]

    tasa_de_ahorro = indicadores["tasa_de_ahorro"]

    aprovechamiento_del_margen_financiero = (
        indicadores["aprovechamiento_del_margen_financiero"]
    )

    estado = (
        evaluacion_financiera["capacidad_de_ahorro"]["estado"]
    )

    # ==========================================================
    # Recomendación según la Tasa de ahorro
    # ==========================================================

    if tasa_de_ahorro >= 0.30:

        recomendaciones.append(
            "Mantener el excelente hábito de destinar una parte importante de los ingresos al ahorro e inversión."
        )

    elif tasa_de_ahorro >= 0.25:

        recomendaciones.append(
            "Continuar fortaleciendo el ahorro para consolidar una mayor estabilidad financiera."
        )

    elif tasa_de_ahorro >= 0.20:

        recomendaciones.append(
            "Mantener el ritmo de ahorro actual y buscar incrementarlo gradualmente."
        )

    elif tasa_de_ahorro >= 0.15:

        recomendaciones.append(
            "Incrementar gradualmente el porcentaje destinado al ahorro."
        )

    elif tasa_de_ahorro >= 0.10:

        recomendaciones.append(
            "Procurar aumentar el ahorro mensual mediante una mejor planificación del presupuesto."
        )

    elif tasa_de_ahorro >= 0.05:

        recomendaciones.append(
            "Priorizar el incremento del ahorro mensual reduciendo gastos no esenciales."
        )

    else:

        recomendaciones.append(
            "Establecer como prioridad aumentar el ahorro mensual para fortalecer la estabilidad financiera."
        )

    # ==========================================================
    # Recomendación según el Aprovechamiento del margen financiero
    # ==========================================================

    if aprovechamiento_del_margen_financiero >= 0.90:

        recomendaciones.append(
            "Mantener el excelente aprovechamiento del margen financiero destinándolo al ahorro o inversión."
        )

    elif aprovechamiento_del_margen_financiero >= 0.75:

        recomendaciones.append(
            "Continuar destinando la mayor parte del margen financiero al ahorro."
        )

    elif aprovechamiento_del_margen_financiero >= 0.60:

        recomendaciones.append(
            "Aprovechar una mayor parte del margen financiero para fortalecer el ahorro."
        )

    elif aprovechamiento_del_margen_financiero >= 0.45:

        recomendaciones.append(
            "Incrementar el porcentaje del margen financiero destinado al ahorro e inversión."
        )

    elif aprovechamiento_del_margen_financiero >= 0.30:

        recomendaciones.append(
            "Reducir gastos discrecionales para aprovechar mejor el margen financiero disponible."
        )

    elif aprovechamiento_del_margen_financiero >= 0.15:

        recomendaciones.append(
            "Destinar una mayor proporción del excedente mensual al ahorro antes de aumentar el consumo."
        )

    else:

        recomendaciones.append(
            "Priorizar el aprovechamiento del margen financiero para construir un fondo de ahorro o inversión."
        )

    # ==========================================================
    # Recomendación según el Estado de la dimensión
    # ==========================================================

    if estado == "Saludable":

        recomendaciones.append(
            "Mantener las estrategias actuales de ahorro para conservar esta fortaleza financiera."
        )

    elif estado == "En observación":

        recomendaciones.append(
            "Dar seguimiento periódico a la capacidad de ahorro para evitar que disminuya con el tiempo."
        )

    else:

        recomendaciones.append(
            "Priorizar el fortalecimiento de la capacidad de ahorro como parte de la planificación financiera personal."
        )

    return recomendaciones

def generar_recomendaciones_endeudamiento(
    indicadores_financieros,
    evaluacion_financiera
):
    """
    Genera las recomendaciones para la dimensión Endeudamiento.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera previamente calculada.

    Retorna:
        list: Lista de recomendaciones para la dimensión.
    """

    recomendaciones = []

    indicadores = indicadores_financieros["endeudamiento"]

    ratio_de_endeudamiento = (
        indicadores["ratio_de_endeudamiento"]
    )

    presion_de_la_deuda = (
        indicadores["presion_de_la_deuda"]
    )

    costo_promedio_del_endeudamiento = (
        indicadores["costo_promedio_del_endeudamiento"]
    )

    estado = (
        evaluacion_financiera["endeudamiento"]["estado"]
    )

    # ==========================================================
    # Recomendación según el Ratio de endeudamiento
    # ==========================================================

    if ratio_de_endeudamiento <= 0.10:

        recomendaciones.append(
            "Mantener el bajo nivel de endeudamiento actual."
        )

    elif ratio_de_endeudamiento <= 0.20:

        recomendaciones.append(
            "Continuar administrando responsablemente las obligaciones financieras."
        )

    elif ratio_de_endeudamiento <= 0.30:

        recomendaciones.append(
            "Vigilar el crecimiento del endeudamiento para mantener una carga financiera saludable."
        )

    elif ratio_de_endeudamiento <= 0.40:

        recomendaciones.append(
            "Reducir gradualmente el porcentaje del ingreso destinado al pago de deudas."
        )

    elif ratio_de_endeudamiento <= 0.50:

        recomendaciones.append(
            "Priorizar la disminución del endeudamiento antes de adquirir nuevas obligaciones financieras."
        )

    elif ratio_de_endeudamiento <= 0.60:

        recomendaciones.append(
            "Elaborar un plan para reducir progresivamente la carga de la deuda."
        )

    else:

        recomendaciones.append(
            "Priorizar la reducción inmediata del endeudamiento para recuperar estabilidad financiera."
        )

    # ==========================================================
    # Recomendación según la Presión de la deuda
    # ==========================================================

    if presion_de_la_deuda <= 0.10:

        recomendaciones.append(
            "Mantener una distribución equilibrada del gasto mensual."
        )

    elif presion_de_la_deuda <= 0.20:

        recomendaciones.append(
            "Continuar controlando el peso de las deudas dentro del presupuesto."
        )

    elif presion_de_la_deuda <= 0.30:

        recomendaciones.append(
            "Vigilar que el pago de deudas no limite otros objetivos financieros."
        )

    elif presion_de_la_deuda <= 0.40:

        recomendaciones.append(
            "Reducir gradualmente la presión de las deudas sobre el presupuesto mensual."
        )

    elif presion_de_la_deuda <= 0.50:

        recomendaciones.append(
            "Reorganizar el presupuesto para disminuir el impacto del pago de deudas."
        )

    elif presion_de_la_deuda <= 0.60:

        recomendaciones.append(
            "Priorizar la disminución de obligaciones financieras para liberar capacidad de gasto."
        )

    else:

        recomendaciones.append(
            "Implementar un plan de reducción de deudas para recuperar flexibilidad financiera."
        )

    # ==========================================================
    # Recomendación según el Costo promedio del endeudamiento
    # ==========================================================

    if costo_promedio_del_endeudamiento == 0:

        recomendaciones.append(
            "Mantener el uso responsable del crédito y evitar adquirir deudas con costos financieros elevados."
        )

    elif costo_promedio_del_endeudamiento <= 10:

        recomendaciones.append(
            "Mantener las condiciones actuales de financiamiento."
        )

    elif costo_promedio_del_endeudamiento <= 20:

        recomendaciones.append(
            "Continuar utilizando fuentes de financiamiento con tasas competitivas."
        )

    elif costo_promedio_del_endeudamiento <= 35:

        recomendaciones.append(
            "Buscar oportunidades para reducir el costo del financiamiento."
        )

    elif costo_promedio_del_endeudamiento <= 50:

        recomendaciones.append(
            "Evaluar alternativas de refinanciamiento con menores tasas de interés."
        )

    elif costo_promedio_del_endeudamiento <= 65:

        recomendaciones.append(
            "Priorizar el pago de las deudas con mayor tasa de interés."
        )

    elif costo_promedio_del_endeudamiento <= 80:

        recomendaciones.append(
            "Reducir el uso de créditos con tasas elevadas y buscar opciones más económicas."
        )

    else:

        recomendaciones.append(
            "Reestructurar o liquidar prioritariamente las deudas con mayor costo financiero."
        )

    # ==========================================================
    # Recomendación según el Estado de la dimensión
    # ==========================================================

    if estado == "Saludable":

        recomendaciones.append(
            "Mantener una administración responsable del endeudamiento para conservar esta fortaleza financiera."
        )

    elif estado == "En observación":

        recomendaciones.append(
            "Dar seguimiento periódico al nivel de endeudamiento para evitar un incremento en el riesgo financiero."
        )

    else:

        recomendaciones.append(
            "Priorizar la reducción del endeudamiento como parte de la estrategia financiera antes de asumir nuevas obligaciones."
        )

    return recomendaciones

def generar_recomendaciones_comportamiento_de_consumo(
    indicadores_financieros,
    evaluacion_financiera,
    variables_globales
):
    """
    Genera las recomendaciones para la dimensión Comportamiento de Consumo.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera previamente calculada.

        variables_globales (dict): Diccionario con las variables
        globales previamente calculadas.

    Retorna:
        list: Lista de recomendaciones para la dimensión.
    """

    consumo_total_por_categoria = (
        variables_globales["consumo_total_por_categoria"]
    )

    # ==========================================================
    # Caso especial:
    # No existen transacciones de consumo
    # ==========================================================

    if consumo_total_por_categoria == 0.0:

        return [

            "Registrar transacciones de consumo de manera consistente para poder evaluar los hábitos financieros."

        ]

    recomendaciones = []

    indicadores = indicadores_financieros["comportamiento_de_consumo"]

    indice_de_concentracion_del_gasto = (
        indicadores["indice_de_concentracion_del_gasto"]
    )

    perfil_de_consumo = indicadores["perfil_de_consumo"]

    predominio_del_gasto = (
        perfil_de_consumo["predominio_del_gasto"]
    )

    diversificacion_del_consumo = (
        perfil_de_consumo["diversificacion_del_consumo"]
    )

    estado = (
        evaluacion_financiera[
            "comportamiento_de_consumo"
        ]["estado"]
    )

    # ==========================================================
    # Recomendación según el Índice de concentración del gasto
    # ==========================================================

    if indice_de_concentracion_del_gasto <= 0.33:

        recomendaciones.append(
            "Mantener una distribución equilibrada del gasto entre las distintas categorías de consumo."
        )

    elif indice_de_concentracion_del_gasto <= 0.66:

        recomendaciones.append(
            "Procurar distribuir el consumo entre más categorías para reducir la dependencia de unos pocos rubros."
        )

    else:

        recomendaciones.append(
            "Revisar la concentración del gasto y buscar una distribución más equilibrada del presupuesto mensual."
        )

    # ==========================================================
    # Recomendación según el Predominio del gasto
    # ==========================================================

    if predominio_del_gasto == (
        "Predominio en gastos esenciales"
    ):

        recomendaciones.append(
            "Mantener la prioridad en los gastos esenciales para fortalecer la estabilidad financiera."
        )

    elif predominio_del_gasto == (
        "Balance entre gastos esenciales y discrecionales"
    ):

        recomendaciones.append(
            "Conservar el equilibrio entre gastos esenciales y discrecionales sin descuidar las necesidades prioritarias."
        )

    else:

        recomendaciones.append(
            "Reducir gradualmente el peso de los gastos discrecionales y priorizar los gastos esenciales."
        )

    # ==========================================================
    # Recomendación según la Diversificación del consumo
    # ==========================================================

    if diversificacion_del_consumo == (
        "Consumo diversificado"
    ):

        recomendaciones.append(
            "Mantener una adecuada diversificación del consumo para reducir la dependencia de una sola categoría."
        )

    else:

        recomendaciones.append(
            "Diversificar gradualmente el consumo para lograr una distribución más equilibrada del presupuesto."
        )

    # ==========================================================
    # Recomendación según el Estado
    # ==========================================================

    if estado == "Saludable":

        recomendaciones.append(
            "Mantener los hábitos actuales de consumo para conservar esta fortaleza financiera."
        )

    elif estado == "En observación":

        recomendaciones.append(
            "Dar seguimiento periódico al comportamiento del consumo para mantener una distribución equilibrada."
        )

    else:

        recomendaciones.append(
            "Priorizar una reorganización del consumo para fortalecer la estabilidad financiera."
        )

    return recomendaciones

def generar_recomendaciones_financieras(
    indicadores_financieros,
    evaluacion_financiera,
    variables_globales
):
    """
    Genera las recomendaciones financieras para las cuatro dimensiones.

    Parámetros:
        indicadores_financieros (dict): Diccionario con los indicadores
        financieros previamente calculados.

        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera previamente calculada.

        variables_globales (dict): Diccionario con las variables
        globales previamente calculadas.

    Retorna:
        dict: Diccionario con las recomendaciones de cada dimensión.
    """

    recomendaciones_balance_financiero = (
        generar_recomendaciones_balance_financiero(
            indicadores_financieros,
            evaluacion_financiera
        )
    )

    recomendaciones_capacidad_de_ahorro = (
        generar_recomendaciones_capacidad_de_ahorro(
            indicadores_financieros,
            evaluacion_financiera
        )
    )

    recomendaciones_endeudamiento = (
        generar_recomendaciones_endeudamiento(
            indicadores_financieros,
            evaluacion_financiera
        )
    )

    recomendaciones_comportamiento_de_consumo = (
        generar_recomendaciones_comportamiento_de_consumo(
            indicadores_financieros,
            evaluacion_financiera,
            variables_globales
        )
    )

    recomendaciones_financieras = {

        "balance_financiero":
            recomendaciones_balance_financiero,

        "capacidad_de_ahorro":
            recomendaciones_capacidad_de_ahorro,

        "endeudamiento":
            recomendaciones_endeudamiento,

        "comportamiento_de_consumo":
            recomendaciones_comportamiento_de_consumo

    }

    return recomendaciones_financieras

def calcular_perfil_financiero(evaluacion_financiera):
    """
    Calcula la puntuación y el estado del perfil financiero general.

    Parámetros:
        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera de las cuatro dimensiones.

    Retorna:
        dict: Diccionario con la puntuación y el estado del perfil
        financiero.
    """

    puntuacion_balance = (
        evaluacion_financiera[
            "balance_financiero"
        ]["puntuacion"]
    )

    puntuacion_ahorro = (
        evaluacion_financiera[
            "capacidad_de_ahorro"
        ]["puntuacion"]
    )

    puntuacion_endeudamiento = (
        evaluacion_financiera[
            "endeudamiento"
        ]["puntuacion"]
    )

    puntuacion_consumo = (
        evaluacion_financiera[
            "comportamiento_de_consumo"
        ]["puntuacion"]
    )

    pesos = PESOS_PERFIL_FINANCIERO

    puntuacion = round(

        (puntuacion_balance *
         pesos["balance_financiero"])

        +

        (puntuacion_ahorro *
         pesos["capacidad_de_ahorro"])

        +

        (puntuacion_endeudamiento *
         pesos["endeudamiento"])

        +

        (puntuacion_consumo *
         pesos["comportamiento_de_consumo"])

    )

    estado = obtener_estado(puntuacion)

    perfil_financiero = {

        "puntuacion": puntuacion,

        "estado": estado

    }

    return perfil_financiero

import os

from google import genai
from dotenv import load_dotenv

# ==========================================================
# Configuración del modelo de lenguaje (Google Gemini)
# ==========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Modelo utilizado para generar la recomendación general.
# Si Google publica una nueva versión, basta con actualizar
# esta constante.

MODELO_LLM = "gemini-flash-latest"

cliente = genai.Client(
    api_key=GEMINI_API_KEY
)

def construir_contexto_llm(
    perfil_financiero,
    evaluacion_financiera,
    recomendaciones_financieras
):
    """
    Construye el contexto que será enviado al modelo de lenguaje (LLM)
    para generar el resumen financiero general.

    Parámetros:
        perfil_financiero (dict): Diccionario con la puntuación y el
        estado general del perfil financiero.

        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera de las cuatro dimensiones.

        recomendaciones_financieras (dict): Diccionario con las
        recomendaciones específicas de cada dimensión.

    Retorna:
        str: Contexto estructurado para el LLM.
    """

    contexto = ""

    # ==========================================================
    # Perfil financiero
    # ==========================================================

    contexto += "PERFIL FINANCIERO\n\n"

    contexto += (
        "Resumen general de la evaluación financiera.\n\n"
    )

    contexto += (
        f"Puntuación: "
        f"{perfil_financiero['puntuacion']}\n"
    )

    contexto += (
        f"Estado: "
        f"{perfil_financiero['estado']}\n\n"
    )

    contexto += "-" * 60 + "\n\n"

    # ==========================================================
    # Evaluación financiera
    # ==========================================================

    contexto += "EVALUACIÓN FINANCIERA\n\n"

    for dimension, datos in evaluacion_financiera.items():

        contexto += f"DIMENSIÓN: {dimension}\n"

        contexto += (
            f"Puntuación: "
            f"{datos['puntuacion']}\n"
        )

        contexto += (
            f"Estado: "
            f"{datos['estado']}\n\n"
        )

    contexto += "-" * 60 + "\n\n"

    # ==========================================================
    # Recomendaciones financieras
    # ==========================================================

    contexto += "RECOMENDACIONES ESPECÍFICAS\n\n"

    for dimension, recomendaciones in recomendaciones_financieras.items():

        contexto += f"DIMENSIÓN: {dimension}\n"

        for recomendacion in recomendaciones:

            contexto += (
                f"- {recomendacion}\n"
            )

        contexto += "\n"

    return contexto

def generar_recomendacion_general(
    perfil_financiero,
    evaluacion_financiera,
    recomendaciones_financieras
):
    """
    Genera un resumen financiero personalizado utilizando un
    modelo de lenguaje (LLM).

    Parámetros:
        perfil_financiero (dict): Diccionario con la puntuación y
        el estado general del perfil financiero.

        evaluacion_financiera (dict): Diccionario con la evaluación
        financiera de las cuatro dimensiones.

        recomendaciones_financieras (dict): Diccionario con las
        recomendaciones específicas de cada dimensión.

    Retorna:
        str: Resumen financiero personalizado generado por el LLM.
    """

    contexto = construir_contexto_llm(
        perfil_financiero,
        evaluacion_financiera,
        recomendaciones_financieras
    )

    prompt = f"""
Eres un asistente especializado en educación financiera.

Tu tarea es redactar un resumen financiero personalizado para el usuario utilizando exclusivamente la información que se proporciona a continuación.

INSTRUCCIONES

- Utiliza únicamente la información proporcionada.
- No inventes indicadores financieros.
- No inventes recomendaciones nuevas.
- No hagas cálculos adicionales.
- No contradigas la evaluación financiera recibida.
- Resume la situación financiera general del usuario de forma clara y coherente.
- Destaca primero las fortalezas financieras del usuario y después menciona los principales aspectos que puede mejorar.
- Prioriza las dimensiones cuyo estado sea "En riesgo" y posteriormente las que estén "En observación".
- Integra de forma natural las recomendaciones específicas ya generadas por el sistema.
- No reformules ni generalices las recomendaciones; exprésalas manteniendo su significado original.
- No infieras recomendaciones adicionales a partir de los indicadores o puntuaciones.
- Evita repetir literalmente una misma palabra o estructura en oraciones consecutivas cuando puedas expresarla de forma natural sin modificar su significado.
- Mantén un tono profesional, claro, cercano y motivador.
- Finaliza el resumen con un mensaje positivo que motive al usuario a continuar mejorando sus hábitos financieros.
- Evita utilizar lenguaje alarmista o generar preocupación innecesaria.
- No utilices listas ni viñetas.
- Escribe un único párrafo.
- La longitud debe estar aproximadamente entre 80 y 120 palabras.

INFORMACIÓN DISPONIBLE

{contexto}

Genera únicamente el resumen financiero.

No agregues títulos, encabezados ni texto adicional.
"""

    try:

        respuesta = cliente.models.generate_content(

            model=MODELO_LLM,

            contents=prompt

        )

        return respuesta.text.strip()

    except Exception:

        return (
            "No fue posible generar la recomendación general debido "
            "a un problema de conexión con el modelo de lenguaje. "
            "Consulte las recomendaciones específicas de cada dimensión."
        )
    

import copy


def construir_resultado_financiero(
    datos_clasificados,
    perfil_financiero,
    indicadores_financieros,
    evaluacion_financiera,
    recomendaciones_financieras,
    recomendacion_general
):
    """
    Construye el diccionario final con el resultado del análisis
    financiero.

    Parámetros:
        datos_clasificados (dict): Información clasificada del usuario.

        perfil_financiero (dict): Perfil financiero general.

        indicadores_financieros (dict): Indicadores financieros de las
        cuatro dimensiones.

        evaluacion_financiera (dict): Evaluación financiera de las cuatro
        dimensiones.

        recomendaciones_financieras (dict): Recomendaciones específicas
        por dimensión.

        recomendacion_general (str): Resumen financiero generado por el
        modelo de lenguaje.

    Retorna:
        dict: Diccionario final del análisis financiero.
    """

    # ==========================================================
    # Diccionario principal
    # ==========================================================

    resultado_financiero = {

        "usuario": {

            "id":
                datos_clasificados["usuario"]["id"],

            "nombre":
                datos_clasificados["usuario"]["nombre"]

        },

        "perfil_financiero": {

            "puntuacion":
                perfil_financiero["puntuacion"],

            "estado":
                perfil_financiero["estado"]

        },

        "dimensiones": {},

        "recomendacion_general":
            recomendacion_general

    }

    # ==========================================================
    # Construcción automática de las dimensiones
    # ==========================================================

    for dimension in indicadores_financieros:

        # Copia independiente para no modificar el motor financiero
        indicadores = copy.deepcopy(
            indicadores_financieros[dimension]
        )

        # ======================================================
        # Adaptación de categorías únicamente para la API
        # ======================================================

        if dimension == "comportamiento_de_consumo":

            distribucion_api = {}

            for categoria, porcentaje in (
                indicadores[
                    "distribucion_del_gasto_por_categoria"
                ].items()
            ):

                distribucion_api[
                    MAPA_CATEGORIAS_API[categoria]
                ] = porcentaje

            indicadores[
                "distribucion_del_gasto_por_categoria"
            ] = distribucion_api

        # ======================================================
        # Construcción de la dimensión
        # ======================================================

        resultado_financiero["dimensiones"][dimension] = {

            "puntuacion":
                evaluacion_financiera[dimension]["puntuacion"],

            "estado":
                evaluacion_financiera[dimension]["estado"],

            "indicadores":
                indicadores,

            "recomendaciones":
                recomendaciones_financieras[dimension]

        }

    return resultado_financiero

def ejecutar_motor_financiero(datos_clasificados):
    """
    Ejecuta el flujo completo del motor financiero.

    Parámetros:
        datos_clasificados (dict): Información financiera clasificada
        del usuario.

    Retorna:
        dict: Resultado completo del análisis financiero.
    """

    # ==========================================================
    # Variables globales
    # ==========================================================

    variables_globales = calcular_variables_globales(
        datos_clasificados
    )

    # ==========================================================
    # Indicadores financieros
    # ==========================================================

    indicadores_financieros = calcular_indicadores_financieros(
        variables_globales,
        datos_clasificados
    )

    # ==========================================================
    # Evaluación financiera
    # ==========================================================

    evaluacion_financiera = calcular_evaluacion_financiera(
        indicadores_financieros,
        variables_globales
    )

    # ==========================================================
    # Perfil financiero
    # ==========================================================

    perfil_financiero = calcular_perfil_financiero(
        evaluacion_financiera
    )

    # ==========================================================
    # Recomendaciones financieras
    # ==========================================================

    recomendaciones_financieras = generar_recomendaciones_financieras(
        indicadores_financieros,
        evaluacion_financiera,
        variables_globales
    )

    # ==========================================================
    # Recomendación general
    # ==========================================================

    recomendacion_general = generar_recomendacion_general(
        perfil_financiero,
        evaluacion_financiera,
        recomendaciones_financieras
    )

    # ==========================================================
    # Resultado final
    # ==========================================================

    resultado_financiero = construir_resultado_financiero(
        datos_clasificados,
        perfil_financiero,
        indicadores_financieros,
        evaluacion_financiera,
        recomendaciones_financieras,
        recomendacion_general
    )

    return resultado_financiero

def funcion_integradora_final (datos):
	datos_clasificados = ejecutar_clasificacion(
    datos_entrada=datos,
    pipeline_movimiento=pipeline_movimiento,
    pipeline_categoria=pipeline_categoria
	)
	resultado_financiero = ejecutar_motor_financiero(datos_clasificados)
	return resultado_financiero

def clasificar_datos(datos):
    datos_clasificados = ejecutar_clasificacion(
        datos_entrada=datos,
        pipeline_movimiento=pipeline_movimiento,
        pipeline_categoria=pipeline_categoria
    )

    return datos_clasificados