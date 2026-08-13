#!/usr/bin/env python
# coding: utf-8

# # **Notebook entregable**
# 
# Incluye:
# 
# - Exploración y limpieza de datos.
# - Tratamiento de variables financieras y textual
# - Ingeniería de características
# - Clasificación de gastos
# - Análisis financiero
# - Entrenamiento y evaluación de modelos
# - Métricas de desempeño
# - Serialización de modelos (.pkl o .joblib)

# # **Modulo clasificación tipo de movimiento y categorías**

# ## **Limpieza y exploración de datos**

# ### **Carga de librerías y dataset**

# In[1]:


import pandas as pd
import unicodedata

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 100)

ruta = "dataset_finance_ai.csv"

df = pd.read_csv(ruta)

print("Dimensiones:", df.shape)
df.head()


# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(
    style="whitegrid",
    palette="deep"
)

plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 11


# In[3]:


df.tail()


# ### **Exploración de las columnas**

# In[4]:


df.info()


# In[5]:


print("Número de filas:", df.shape[0])
print("Número de columnas:", df.shape[1])
print("Número de usuarios:", df["user_id"].nunique())

print("\nColumnas:")
print(df.columns.tolist())


# In[6]:


df.sample(10, random_state=42)


# ### **Exploración de valores nulos**

# In[7]:


nulos = pd.DataFrame({
    "nulos": df.isna().sum(),
    "porcentaje": (df.isna().mean() * 100).round(2)
})

nulos


# In[8]:


df[["categoria", "grupo", "tasa_de_interes_de_la_tarjeta"]].isna().sum()


# ##### **nan en categoria**

# In[9]:


pd.crosstab(
    df["tipo_movimiento"],
    df["categoria"].isna(),
    margins=True
)


# In[10]:


df[
    (df["tipo_movimiento"] != "Consumo") &
    (df["categoria"].notna())
].shape[0]


# Los nan se encuentran presentes en Ahorro e Inversión, Ingreso y Pago de deuda, las cuales son dimensiones que estructuralmente no tienen categroría porque no son consumo.

# ##### **nan en grupo**

# In[11]:


pd.crosstab(
    df["tipo_movimiento"],
    df["grupo"].isna(),
    margins=True
)


# In[12]:


df[df["categoria"] == "Otros"]["grupo"].value_counts(dropna=False)


# Hay un total de 655 nan en grupo. 528 son de las dimensiones diferentes a consumo que no necesitan "categoría" y por lo tanto no pueden clasificarse en "esencial" o "discrecional" + 127 pertenecientes a "otros", que por default no puedes categorizarse.
# 
# Por lo tanto, al no ser errores, no deben imputarse, puesto que tienen sentido lógico dentro de la estructura.
# 

# ### **Exploración tasa de interés**

# Tada de interes unicamente sale cuando tipo_pago = tarjeta de credito

# In[13]:


pd.crosstab(
    df["tipo_pago"],
    df["tasa_de_interes_de_la_tarjeta"].isna(),
    margins=True
)


# In[14]:


credito_sin_tasa = df[
    (df["tipo_pago"] == "Tarjeta de crédito") &
    (df["tasa_de_interes_de_la_tarjeta"].isna())
]

tasa_sin_credito = df[
    (df["tipo_pago"] != "Tarjeta de crédito") &
    (df["tasa_de_interes_de_la_tarjeta"].notna())
]

print("Créditos sin tasa:", len(credito_sin_tasa))
print("Operaciones no crédito con tasa:", len(tasa_sin_credito))


# No se debe imputar esta variable puesto que en todos los casos la tasa de interés sí aparece unicamente en entradas de tarjeta de credito como tipo de pago.

# ### **Duplicados**

# In[15]:


duplicados = df.duplicated().sum()

print("Registros duplicados:", duplicados)


# ### **Validación de identificadores del usuario**

# In[16]:


print("Usuarios únicos:", df["user_id"].nunique())
print("IDs nulos:", df["user_id"].isna().sum())


# In[17]:


validacion_usuario = (
    df.groupby("user_id")
      .agg(
          nombres=("nombre", "nunique"),
          perfiles=("arquetipo_perfil", "nunique")
      )
)

validacion_usuario.describe()


# In[18]:


validacion_usuario[
    (validacion_usuario["nombres"] > 1) |
    (validacion_usuario["perfiles"] > 1)
]


# ### **Validación de fechas**

# In[19]:


columnas_fecha = [
    "periodo_inicio",
    "periodo_fin",
    "fecha"
]

for columna in columnas_fecha:
    df[columna] = pd.to_datetime(
        df[columna],
        format="%Y-%m-%d",
        errors="raise"
    )


# In[20]:


for columna in columnas_fecha:
    print(
        columna,
        df[columna].min(),
        df[columna].max()
    )


# In[21]:


fuera_periodo = df[
    (df["fecha"] < df["periodo_inicio"]) |
    (df["fecha"] > df["periodo_fin"])
]

print("Transacciones fuera del periodo:", len(fuera_periodo))


# ### **Validación de monto**

# In[22]:


df["monto"] = pd.to_numeric(
    df["monto"],
    errors="raise"
).round(2)


# In[23]:


print("Montos nulos:", df["monto"].isna().sum())
print("Montos en cero:", (df["monto"] == 0).sum())
print("Montos negativos:", (df["monto"] < 0).sum())


# In[24]:


df["monto"].describe()


# ### **Outliers**

# In[25]:


Q1 = df["monto"].quantile(0.25)
Q3 = df["monto"].quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Límite inferior:", limite_inferior)
print("Límite superior:", limite_superior)


# In[26]:


outliers = df[
    (df["monto"] < limite_inferior) |
    (df["monto"] > limite_superior)
]

print("Número de posibles outliers:", len(outliers))

outliers.sort_values(
    "monto",
    ascending=False
).head(20)


# El ingreso de $300,000 puede ser extraño respecto a la distribución general pero perfectamente válido para alguno de los perfiles.

# In[27]:


#Inspecciona por tipo de movimientos
for tipo, datos in df.groupby("tipo_movimiento"):

    Q1 = datos["monto"].quantile(0.25)
    Q3 = datos["monto"].quantile(0.75)
    IQR = Q3 - Q1

    limite_superior = Q3 + 1.5 * IQR

    n_outliers = (datos["monto"] > limite_superior).sum()

    print(
        f"{tipo}: "
        f"{n_outliers} posibles outliers | "
        f"Límite: ${limite_superior:,.2f} | "
        f"Máximo: ${datos['monto'].max():,.2f}"
    )


# ### **Tratamiento de las variables de texto**

# In[28]:


columnas_texto = [
    "nombre",
    "arquetipo_perfil",
    "descripcion",
    "tipo_movimiento",
    "categoria",
    "grupo",
    "tipo_pago"
]

for columna in columnas_texto:

    mask = df[columna].notna()

    df.loc[mask, columna] = (
        df.loc[mask, columna]
          .astype(str)
          .str.strip()
          .str.replace(r"\s+", " ", regex=True)
    )


# ### **Creación variable descripcion_limpia**

# In[29]:


def limpiar_descripcion(texto):

    texto = unicodedata.normalize("NFC", texto)

    texto = texto.strip().lower()

    texto = " ".join(texto.split())

    return texto


df["descripcion_limpia"] = df["descripcion"].apply(
    limpiar_descripcion
)


# In[30]:


df[
    ["descripcion", "descripcion_limpia"]
].sample(10, random_state=30)


# ### **Distribución de tipos de movimiento**

# In[31]:


conteo_movimientos = (
    df["tipo_movimiento"]
    .value_counts()
    .to_frame("cantidad")
)

conteo_movimientos["porcentaje"] = (
    conteo_movimientos["cantidad"]
    / len(df)
    * 100
).round(2)

conteo_movimientos


# Aunque hay un fuerte desbalance de clases, esto es normal pues en la vida real, las personas suelen tener muchos más gastos que ingresos. Es decir la cantidad total invertida en gastos/consumo se divide en más partes que la cantidad total del ingreso.

# In[32]:


plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data=conteo_movimientos,
    x="tipo_movimiento",
    y="cantidad",
    hue="tipo_movimiento",
    legend=False,
    palette="Blues_d"
)

for i, fila in conteo_movimientos.iterrows():
    ax.text(
        i,
        fila["cantidad"] + 50,
        f'{fila["cantidad"]:,}\n({fila["porcentaje"]:.1f}%)',
        ha="center",
        fontsize=10
    )

plt.title("Distribución de transacciones por tipo de movimiento")
plt.xlabel("Tipo de movimiento")
plt.ylabel("Número de transacciones")

plt.tight_layout()
plt.show()


# Se observa un fuerte desbalance en la variable objetivo tipo_movimiento. El 88.71% de las transacciones corresponden a Consumo, mientras que Ahorro e inversión representa únicamente el 2.33%. Esta distribución deberá considerarse posteriormente durante el entrenamiento y evaluación del clasificador, ya que la exactitud por sí sola podría producir una evaluación engañosa.

# ### **Comparación de clases con escala logarítmica**

# In[33]:


plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    y="tipo_movimiento",
    order=df["tipo_movimiento"].value_counts().index,
    hue="tipo_movimiento",
    legend=False,
    palette="Set2"
)

plt.xscale("log")

plt.title("Desbalance de clases en tipo de movimiento")
plt.xlabel("Número de transacciones - escala logarítmica")
plt.ylabel("Tipo de movimiento")

plt.tight_layout()
plt.show()


# Debido al desbalance de clases tan marcado no se podrá evaluar el clasificador únicamente con accuracy_score(), se necesitará classification_report(), confusion_matrix(), f1_score(..., average="macro").

# ### **Distribución de categorías de consumo**

# In[34]:


df_consumo = df[
    df["tipo_movimiento"] == "Consumo"
].copy()


# In[35]:


distribucion_categorias = (
    df_consumo["categoria"]
    .value_counts()
    .to_frame("cantidad")
)

distribucion_categorias["porcentaje"] = (
    distribucion_categorias["cantidad"]
    / len(df_consumo)
    * 100
).round(2)

distribucion_categorias


# In[36]:


plt.figure(figsize=(10, 7))

ax = sns.barplot(
    data=distribucion_categorias,
    y="categoria",
    x="cantidad",
    hue="categoria",
    legend=False,
    palette="viridis"
)

for i, fila in distribucion_categorias.iterrows():
    ax.text(
        fila["cantidad"] + 15,
        i,
        f'{fila["porcentaje"]:.1f}%',
        va="center"
    )

plt.title("Distribución de categorías dentro de Consumo")
plt.xlabel("Número de transacciones")
plt.ylabel("Categoría")

plt.tight_layout()
plt.show()


# La distribución de categorías también presenta desbalance. Alimentación y Transporte concentran aproximadamente el 64.44% de las transacciones de consumo, mientras que Viajes y vacaciones representa solamente el 2.05%. Por lo tanto, será necesario utilizar métricas sensibles al desempeño de las clases minoritarias.
# *Uso de macro F1-score.

# ### **Frecuencia vs dinero gastado por categoría**

# In[37]:


gasto_categoria = (
    df_consumo
    .groupby("categoria")["monto"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

gasto_categoria["porcentaje"] = (
    gasto_categoria["monto"]
    / gasto_categoria["monto"].sum()
    * 100
)


# In[38]:


plt.figure(figsize=(10, 7))

ax = sns.barplot(
    data=gasto_categoria,
    y="categoria",
    x="porcentaje",
    hue="categoria",
    legend=False,
    palette="crest"
)

for i, fila in gasto_categoria.iterrows():
    ax.text(
        fila["porcentaje"] + 0.3,
        i,
        f'{fila["porcentaje"]:.1f}%',
        va="center"
    )

plt.title("Participación del gasto total por categoría")
plt.xlabel("Porcentaje del gasto total (%)")
plt.ylabel("Categoría")

plt.tight_layout()
plt.show()


# Vivienda representa solamente 6.29% de las transacciones de consumo, pero concentra 16.06% del monto gastado. Esto refleja que la frecuencia de las transacciones y su impacto económico son fenómenos diferentes.

# ### **Distribución de grupos**

# In[39]:


df_consumo["grupo"].value_counts(
    dropna=False
)


# In[40]:


df_consumo["grupo"].value_counts(
    normalize=True,
    dropna=False
).mul(100).round(2)


# ### **Análisis de montos por movimiento**

# In[41]:


df.groupby("tipo_movimiento")["monto"].agg([
    "count",
    "mean",
    "median",
    "std",
    "min",
    "max"
]).round(2)


# In[42]:


#utiliza escala logarítmica para evitar que la gráfica se aplaste por el ingreso de ~300,000
plt.figure(figsize=(11, 6))

sns.boxplot(
    data=df,
    x="tipo_movimiento",
    y="monto",
    hue="tipo_movimiento",
    legend=False,
    palette="Set2"
)

plt.yscale("log")

plt.title("Distribución de montos por tipo de movimiento")
plt.xlabel("Tipo de movimiento")
plt.ylabel("Monto ($) - escala logarítmica")

plt.tight_layout()
plt.show()


# Las distribuciones de los montos presentan una fuerte asimetría positiva. Los valores extremos fueron conservados debido a que corresponden a comportamientos financieros plausibles de los perfiles simulados.

# ### **Montos por categoría**

# In[43]:


df_consumo.groupby("categoria")["monto"].agg([
    "count",
    "mean",
    "median",
    "min",
    "max"
]).round(2).sort_values(
    "median",
    ascending=False
)


# frecuencia de la categoría ≠ cantidad de dinero gastado

# ### **Distribución por tipo de pago**

# In[44]:


df["tipo_pago"].unique()


# In[45]:


distribucion_tipo_pago = (
    df["tipo_pago"]
    .value_counts()
    .to_frame("cantidad")
)

distribucion_tipo_pago["porcentaje"] = (
    distribucion_tipo_pago["cantidad"]
    / len(df)
    * 100
).round(2)

distribucion_tipo_pago


# In[46]:


plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data=distribucion_tipo_pago,
    y="tipo_pago",
    x="cantidad",
    hue="tipo_pago",
    legend=False,
    palette="mako"
)

for i, fila in distribucion_tipo_pago.iterrows():
    ax.text(
        fila["cantidad"] + 15,
        i,
        f'{fila["porcentaje"]:.1f}%',
        va="center"
    )

plt.title("Distribución de transacciones por medio de pago")
plt.xlabel("Número de transacciones")
plt.ylabel("Medio de pago")

plt.tight_layout()
plt.show()


# ### **Relación entre movimiento y medio de pago**

# In[47]:


movimiento_pago = pd.crosstab(
    df["tipo_movimiento"],
    df["tipo_pago"],
    normalize="index"
) * 100

movimiento_pago.round(1)


# In[48]:


plt.figure(figsize=(11, 5))

sns.heatmap(
    movimiento_pago,
    annot=True,
    fmt=".1f",
    cmap="Blues",
    cbar_kws={"label": "% dentro del tipo de movimiento"}
)

plt.title("Relación entre tipo de movimiento y medio de pago")
plt.xlabel("Medio de pago")
plt.ylabel("Tipo de movimiento")

plt.tight_layout()
plt.show()


# Los consumos se distribuyen aproximadamente:
# 
# - Débito: 45.0%
# - Transferencia: 21.8%
# - Crédito: 19.9%
# - Efectivo: 13.3%
# 
# Mientras que ahorro, inversión y pago de deuda se realizan mediante transferencia en el dataset.
# 
# Esto es importante para el modelo porque tipo_pago podría convertirse en una variable altamente predictiva.

# ### **Análisis de tipo de pago = tarjeta de crédito**

# In[49]:


df_credito = df[
    df["tipo_pago"] == "Tarjeta de crédito"
].copy()


# In[50]:


df_credito["tasa_de_interes_de_la_tarjeta"].describe().round(2)


# ### **Distribución de tasas de tarjeta de crédito**

# In[51]:


plt.figure(figsize=(10, 6))

sns.histplot(
    data=df_credito,
    x="tasa_de_interes_de_la_tarjeta",
    bins=15,
    kde=True,
    color="steelblue"
)

plt.axvline(
    df_credito["tasa_de_interes_de_la_tarjeta"].median(),
    color="red",
    linestyle="--",
    label=f'Mediana: {df_credito["tasa_de_interes_de_la_tarjeta"].median():.1f}%'
)

plt.title("Distribución de tasas de interés de tarjetas de crédito")
plt.xlabel("Tasa de interés (%)")
plt.ylabel("Frecuencia")
plt.legend()

plt.tight_layout()
plt.show()


# **Esta variable es más útil para caracterización financiera que para el clasificador semántico.**

# ### **Cantidad de transacciones por usuario**

# In[52]:


transacciones_usuario = (
    df.groupby("user_id")
    .size()
    .reset_index(name="numero_transacciones")
)


# In[53]:


plt.figure(figsize=(10, 6))

sns.histplot(
    data=transacciones_usuario,
    x="numero_transacciones",
    bins=15,
    kde=True,
    color="teal"
)

plt.axvline(
    transacciones_usuario["numero_transacciones"].median(),
    color="red",
    linestyle="--",
    label=f'Mediana: {transacciones_usuario["numero_transacciones"].median():.0f}'
)

plt.title("Distribución del número de transacciones por usuario")
plt.xlabel("Número de transacciones mensuales")
plt.ylabel("Número de usuarios")
plt.legend()

plt.tight_layout()
plt.show()


# - Mínimo:     3 transacciones
# - Mediana:   44
# - Promedio:  42.51
# - Máximo:    74

# ### **Repetición en las descripciones**

# In[54]:


#comprueba la diversidad de las descripciones
print(
    "Transacciones:",
    len(df)
)

print(
    "Descripciones únicas:",
    df["descripcion"].nunique()
)

print(
    "Descripciones limpias únicas:",
    df["descripcion_limpia"].nunique()
)


# In[55]:


#comprueba la repitición
frecuencia_descripciones = (
    df["descripcion_limpia"]
    .value_counts()
    .reset_index()
)

frecuencia_descripciones.columns = [
    "descripcion_limpia",
    "frecuencia"
]

frecuencia_descripciones.head(20)


# In[56]:


plt.figure(figsize=(10, 6))

sns.histplot(
    data=frecuencia_descripciones,
    x="frecuencia",
    bins=25,
    color="darkorange"
)

plt.title("Frecuencia de repetición de las descripciones")
plt.xlabel("Número de veces que aparece una descripción")
plt.ylabel("Número de descripciones únicas")

plt.tight_layout()
plt.show()


# Existen descripciones idénticas repetidas en múltiples transacciones. Por lo tanto, una división aleatoria convencional podría colocar la misma descripción tanto en entrenamiento como en prueba, generando fuga de información y una estimación excesivamente optimista del desempeño.

# ### **Contradicciones semánticas**
# 
# Comprueba si una descripción tiene diferentes etiquetas

# In[57]:


#para tipo de movimiento
conflictos_movimiento = (
    df.groupby("descripcion_limpia")
      ["tipo_movimiento"]
      .nunique()
)

conflictos_movimiento = conflictos_movimiento[
    conflictos_movimiento > 1
]

print(
    "Descripciones con múltiples tipos de movimiento:",
    len(conflictos_movimiento)
)


# In[58]:


#para las categorías
conflictos_categoria = (
    df_consumo.groupby("descripcion_limpia")
              ["categoria"]
              .nunique()
)

conflictos_categoria = conflictos_categoria[
    conflictos_categoria > 1
]

print(
    "Descripciones con múltiples categorías:",
    len(conflictos_categoria)
)


# ### **Comportamiento temporal de las transacciones**
# Comprueba que las transacciones se distribuyan durante el mes.

# In[59]:


transacciones_dia = (
    df.groupby("fecha")
    .size()
    .reset_index(name="transacciones")
)


# In[60]:


plt.figure(figsize=(12, 6))

sns.lineplot(
    data=transacciones_dia,
    x="fecha",
    y="transacciones",
    marker="o",
    linewidth=2
)

plt.title("Número de transacciones por día")
plt.xlabel("Fecha")
plt.ylabel("Número de transacciones")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# Esta visualización sirve principalmente para validar que las transacciones no fueron colocadas todas artificialmente en los mismos días.

# ### **Validación final**

# In[61]:


print("Dimensiones finales:", df.shape)
print("Usuarios:", df["user_id"].nunique())
print("Duplicados:", df.duplicated().sum())
print("Descripciones vacías:", (df["descripcion_limpia"] == "").sum())
print("Montos <= 0:", (df["monto"] <= 0).sum())

print("\nNulos:")
print(df.isna().sum())


# ### **Exportación del dataset limpio**

# In[62]:


df.to_csv(
    "dataset_finance_ai_110_usuarios_limpio.csv",
    index=False,
    encoding="utf-8"
)


# ## **Conclusiones del análisis exploratorio**
# 
# El análisis exploratorio muestra que el dataset presenta distribuciones financieras heterogéneas tanto en frecuencia como en monto. Los movimientos de Consumo representan el 88.71% de las observaciones, evidenciando un fuerte desbalance respecto a Ingreso, Pago de deuda y Ahorro e inversión. Dentro de los consumos, Alimentación y Transporte concentran el 64.44% de las transacciones.
# 
# Los montos presentan distribuciones asimétricas y valores extremos que se consideran plausibles dadas las características de los perfiles financieros simulados, por lo que no fueron eliminados. Asimismo, se identificó una repetición considerable de las descripciones textuales: las 4,676 transacciones contienen 535 descripciones únicas, algunas repetidas hasta 75 veces.
# 
# Este último hallazgo es relevante para el desarrollo del modelo de clasificación, ya que una separación aleatoria de los datos podría colocar descripciones idénticas simultáneamente en entrenamiento y prueba, provocando fuga de información. Por lo tanto, la estrategia de partición deberá considerar agrupamiento por descripción y métricas robustas ante el desbalance de clases, especialmente macro F1-score.

# # **Preparación de datos para el modelado**

# **Objetivo:**
# 
# En esta etapa, el sistema estará compuesto por dos tareas supervisadas independientes. La primera corresponde a la **clasificación del movimiento**, para la cual se utilizarán todas las transacciones disponibles. En este caso, la variable objetivo será `tipo_movimiento`, que contempla cuatro clases posibles (Ingreso, Consumo, Ahorro e inversión y PAgo de deuda). La segunda tarea será la **clasificación del consumo**, que se aplicará únicamente a aquellos movimientos previamente identificados como Consumo. Para esta tarea, la variable objetivo será `categoria`, compuesta por diez clases (Alimentación, Vivienda, Transporte, Educación, etc).
# 
# En ambas tareas, la principal variable de entrada será `  descripcion_limpia`. Esta variable contiene la representación textual de la descripción de cada transacción después del proceso de limpieza y será la fuente de información utilizada por los modelos para realizar la clasificación semántica.
# 
# La lógica del sistema se organizará de manera secuencial. En primer lugar, la descripción de la transacción será procesada por el clasificador de movimiento, encargado de determinar el tipo de movimiento correspondiente. Posteriormente, el sistema verificará si el movimiento ha sido clasificado como Consumo. Si pertenece a otro tipo de movimiento, el proceso de clasificación finalizará en ese punto. En cambio, si se identifica como Consumo, la transacción será enviada a un segundo clasificador, cuya función será determinar la categoría de consumo correspondiente.
# 
# Para evitar posibles problemas de fuga de información (*data leakage*) y garantizar que las predicciones se basen principalmente en el contenido semántico de las transacciones, las variables `user_id`, `nombre`, `arquetipo_perfil`, `grupo` y cualquier otra variable que revele directa o indirectamente la etiqueta que se desea predecir. Asimismo, `categoria` no será utilizada como característica durante la predicción del tipo de movimiento.
# 
# Estas columnas se conservaron en el conjunto de datos; sin embargo, no serán utilizadas para entrenar y ejecutar los modelos de clasificación semántica.

# ## **Importación de librerías y carga del dataset limpio**

# In[63]:


from sklearn.model_selection import StratifiedGroupKFold

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 100)

RANDOM_STATE = 42


# In[64]:


ruta_dataset = "dataset_finance_ai_110_usuarios_limpio.csv"

df = pd.read_csv(
    ruta_dataset,
    parse_dates=[
        "periodo_inicio",
        "periodo_fin",
        "fecha"
    ]
)

print("Dimensiones:", df.shape)
print("Usuarios:", df["user_id"].nunique())
print("Descripciones únicas:", df["descripcion_limpia"].nunique())

df.head()


# In[65]:


#valida variables necesarias
columnas_necesarias = [
    "descripcion_limpia",
    "tipo_movimiento",
    "categoria"
]

df[columnas_necesarias].isna().sum()


# In[66]:


#valida las descripciones
assert df["descripcion_limpia"].notna().all()
assert df["descripcion_limpia"].str.strip().ne("").all()

print("Todas las descripciones son válidas.")


# In[67]:


#valida las categorias
assert df["descripcion_limpia"].notna().all()
assert df["descripcion_limpia"].str.strip().ne("").all()

print("Todas las descripciones son válidas.")


# ## **Tarea 1: Clasificación del movimiento**

# ### **Preparación del dataset**

# In[68]:


columnas_tarea_movimiento = [
    "user_id",
    "descripcion",
    "descripcion_limpia",
    "tipo_movimiento"
]

datos_movimiento = df[
    columnas_tarea_movimiento
].copy()

print("Registros:", len(datos_movimiento))
print("Descripciones únicas:", datos_movimiento["descripcion_limpia"].nunique())

datos_movimiento.head()


# In[69]:


objetivo_movimiento = "tipo_movimiento"


# In[70]:


datos_movimiento[
    objetivo_movimiento
].value_counts()


# ### **Split agrupado**
# 
# Utilizar 'train_test_split' aleatorio podría colocar la misma descripción tanto en el conjunto de entrenamiento como en el de prueba, haciendo así que el modelo no aprendiera nada nuevo sino que sólo reconocería frases que ya vio antes.
# 
# Por lo tanto, con la finalidad de mantener las proporciones de cada clase y la descripción completa en un sólo grupo, se usará StratifiedGroupKFold.

# In[71]:


def crear_split_agrupado(
    datos,
    columna_objetivo,
    columna_grupo="descripcion_limpia",
    n_splits=5,
    random_state=42
):
    """
    Genera una división aproximada 80/20:

    - Estratificada por la variable objetivo.
    - Agrupada por descripción.
    - Sin descripciones compartidas entre train y test.
    """

    splitter = StratifiedGroupKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state
    )

    X_temporal = datos[[columna_grupo]]
    y = datos[columna_objetivo]
    grupos = datos[columna_grupo]

    train_indices, test_indices = next(
        splitter.split(
            X=X_temporal,
            y=y,
            groups=grupos
        )
    )

    datos_train = (
        datos.iloc[train_indices]
        .copy()
        .reset_index(drop=True)
    )

    datos_test = (
        datos.iloc[test_indices]
        .copy()
        .reset_index(drop=True)
    )

    return datos_train, datos_test


# ### **Split de movimientos**

# In[72]:


train_movimiento, test_movimiento = crear_split_agrupado(
    datos=datos_movimiento,
    columna_objetivo="tipo_movimiento",
    random_state=RANDOM_STATE
)


# In[73]:


#revisa tamaños
print("Train:", train_movimiento.shape)
print("Test:", test_movimiento.shape)

print(
    "Porcentaje train:",
    round(len(train_movimiento) / len(datos_movimiento) * 100, 2)
)

print(
    "Porcentaje test:",
    round(len(test_movimiento) / len(datos_movimiento) * 100, 2)
)


# ### **Verifica que no exista fuga por descripción**

# In[74]:


descripciones_train_movimiento = set(
    train_movimiento["descripcion_limpia"]
)

descripciones_test_movimiento = set(
    test_movimiento["descripcion_limpia"]
)

descripciones_compartidas_movimiento = (
    descripciones_train_movimiento
    .intersection(descripciones_test_movimiento)
)

print(
    "Descripciones únicas en train:",
    len(descripciones_train_movimiento)
)

print(
    "Descripciones únicas en test:",
    len(descripciones_test_movimiento)
)

print(
    "Descripciones compartidas:",
    len(descripciones_compartidas_movimiento)
)


# In[75]:


#validación automática
assert len(descripciones_compartidas_movimiento) == 0

print("Split correcto: no existe fuga por descripción.")


# ### **Compara la distribución de las clases**

# In[76]:


def comparar_distribuciones(
    datos_completos,
    datos_train,
    datos_test,
    columna_objetivo
):
    distribucion = pd.concat(
        [
            datos_completos[columna_objetivo]
            .value_counts()
            .rename("total"),

            datos_train[columna_objetivo]
            .value_counts()
            .rename("train"),

            datos_test[columna_objetivo]
            .value_counts()
            .rename("test"),

            (
                datos_completos[columna_objetivo]
                .value_counts(normalize=True)
                .mul(100)
                .round(2)
                .rename("total_pct")
            ),

            (
                datos_train[columna_objetivo]
                .value_counts(normalize=True)
                .mul(100)
                .round(2)
                .rename("train_pct")
            ),

            (
                datos_test[columna_objetivo]
                .value_counts(normalize=True)
                .mul(100)
                .round(2)
                .rename("test_pct")
            )
        ],
        axis=1
    )

    return distribucion


# In[77]:


distribucion_movimiento = comparar_distribuciones(
    datos_completos=datos_movimiento,
    datos_train=train_movimiento,
    datos_test=test_movimiento,
    columna_objetivo="tipo_movimiento"
)

distribucion_movimiento


# ### **Valida cobertura de clases**

# In[78]:


clases_totales_movimiento = set(
    datos_movimiento["tipo_movimiento"].unique()
)

clases_train_movimiento = set(
    train_movimiento["tipo_movimiento"].unique()
)

clases_test_movimiento = set(
    test_movimiento["tipo_movimiento"].unique()
)

assert clases_totales_movimiento.issubset(
    clases_train_movimiento
)

assert clases_totales_movimiento.issubset(
    clases_test_movimiento
)

print("Todas las clases están presentes en train y test.")


# ## **Tarea 2: Clasificación de categoría**

# ### **Selección de consumos**
# 
# Categoría si y sólo si el movimiento es consumo

# In[79]:


datos_categoria = (
    df.loc[
        df["tipo_movimiento"] == "Consumo",
        [
            "user_id",
            "descripcion",
            "descripcion_limpia",
            "categoria",
            "grupo",
            "tipo_pago",
            "monto"
        ]
    ]
    .copy()
    .reset_index(drop=True)
)


# In[80]:


#valida datos_categoria
print("Registros de consumo:", len(datos_categoria))
print("Categorías:", datos_categoria["categoria"].nunique())
print("Descripciones únicas:", datos_categoria["descripcion_limpia"].nunique())

assert datos_categoria["categoria"].notna().all()


# In[81]:


#La variable objetivo será:
objetivo_categoria = "categoria"


# ### **Split agrupado de cateegorías**

# In[82]:


train_categoria, test_categoria = crear_split_agrupado(
    datos=datos_categoria,
    columna_objetivo="categoria",
    random_state=RANDOM_STATE
)


# In[83]:


print("Train:", train_categoria.shape)
print("Test:", test_categoria.shape)

print(
    "Porcentaje train:",
    round(len(train_categoria) / len(datos_categoria) * 100, 2)
)

print(
    "Porcentaje test:",
    round(len(test_categoria) / len(datos_categoria) * 100, 2)
)


# ### **Verifica ausencia de fuga en categoría**

# In[84]:


descripciones_train_categoria = set(
    train_categoria["descripcion_limpia"]
)

descripciones_test_categoria = set(
    test_categoria["descripcion_limpia"]
)

descripciones_compartidas_categoria = (
    descripciones_train_categoria
    .intersection(descripciones_test_categoria)
)

print(
    "Descripciones únicas en train:",
    len(descripciones_train_categoria)
)

print(
    "Descripciones únicas en test:",
    len(descripciones_test_categoria)
)

print(
    "Descripciones compartidas:",
    len(descripciones_compartidas_categoria)
)

assert len(descripciones_compartidas_categoria) == 0


# ### **Compara las reglas entre entrenamiento y prueba**

# In[85]:


distribucion_categoria = comparar_distribuciones(
    datos_completos=datos_categoria,
    datos_train=train_categoria,
    datos_test=test_categoria,
    columna_objetivo="categoria"
)

distribucion_categoria


# ### **Verifica la cobertura de las 10 categorías**

# In[86]:


categorias_totales = set(
    datos_categoria["categoria"].unique()
)

categorias_train = set(
    train_categoria["categoria"].unique()
)

categorias_test = set(
    test_categoria["categoria"].unique()
)

assert categorias_totales.issubset(categorias_train)
assert categorias_totales.issubset(categorias_test)

print("Todas las categorías están presentes en train y test.")


# ### **Preparación de variables que recibirá TF-IDF**

# #### **Clasificador de tipo de movimiento**

# In[87]:


#separa x y y
X_train_movimiento = (
    train_movimiento["descripcion_limpia"]
    .copy()
)

X_test_movimiento = (
    test_movimiento["descripcion_limpia"]
    .copy()
)

y_train_movimiento = (
    train_movimiento["tipo_movimiento"]
    .copy()
)

y_test_movimiento = (
    test_movimiento["tipo_movimiento"]
    .copy()
)


# #### **Clasificador de categoría**

# In[88]:


#separa x y y
X_train_categoria = (
    train_categoria["descripcion_limpia"]
    .copy()
)

X_test_categoria = (
    test_categoria["descripcion_limpia"]
    .copy()
)

y_train_categoria = (
    train_categoria["categoria"]
    .copy()
)

y_test_categoria = (
    test_categoria["categoria"]
    .copy()
)


# In[89]:


#revisa las dimensiones

print("Clasificador de movimiento")
print("X train:", X_train_movimiento.shape)
print("X test:", X_test_movimiento.shape)
print("y train:", y_train_movimiento.shape)
print("y test:", y_test_movimiento.shape)

print("\nClasificador de categoría")
print("X train:", X_train_categoria.shape)
print("X test:", X_test_categoria.shape)
print("y train:", y_train_categoria.shape)
print("y test:", y_test_categoria.shape)


# #### **Verificación final automatizada**
# 
# Esta celda detendrá todo el notebook si el dataset llega a cambiar y el split deja de cumplir las condiciones.
# 

# In[90]:


# Sin valores faltantes en el texto
assert X_train_movimiento.notna().all()
assert X_test_movimiento.notna().all()
assert X_train_categoria.notna().all()
assert X_test_categoria.notna().all()

# Sin textos vacíos
assert X_train_movimiento.str.strip().ne("").all()
assert X_test_movimiento.str.strip().ne("").all()
assert X_train_categoria.str.strip().ne("").all()
assert X_test_categoria.str.strip().ne("").all()

# Sin descripciones compartidas
assert set(X_train_movimiento).isdisjoint(
    set(X_test_movimiento)
)

assert set(X_train_categoria).isdisjoint(
    set(X_test_categoria)
)

# Todas las clases representadas
assert set(y_train_movimiento.unique()) == set(
    y_test_movimiento.unique()
)

assert set(y_train_categoria.unique()) == set(
    y_test_categoria.unique()
)

print("Preparación terminada correctamente.")
print("No existe solapamiento de descripciones entre train y test.")
print("Todas las clases están representadas.")


# Se definieron dos tareas de clasificación: la identificación del tipo de movimiento para todas las transacciones y la clasificación de categoría exclusivamente para los movimientos de Consumo. En ambas tareas se utilizó descripcion_limpia como variable de entrada.
# 
# Para evitar fuga de información causada por la repetición de descripciones, se empleó una partición estratificada y agrupada mediante StratifiedGroupKFold. Este procedimiento aseguró que cada descripción apareciera exclusivamente en entrenamiento o prueba, manteniendo al mismo tiempo proporciones similares de las clases.
# 
# Para el clasificador de movimientos se obtuvieron 3,740 registros de entrenamiento y 936 de prueba, con cero descripciones compartidas. Para el clasificador de categorías se obtuvieron 3,316 registros de entrenamiento y 832 de prueba, igualmente sin solapamiento. Todas las clases permanecieron representadas en ambos conjuntos.

# ### **Extracción de características con TF-IDF**
# 
# En este bloque se converitrán las descripciones en matrices numéricas. Después de auditar una primera versión basada únicamente en palabras, se procederá con:
# 
# - TF-IDF de palabras y bigramas, para capturar expresiones como pago tarjeta o compré comida.
# - TF-IDF de caracteres, para capturar variaciones como pago, pagué, pagando, plurales y diferencias ortográficas.
# 
# TF-IDF asigna mayor importancia a términos que aparecen en una descripción o no aparecen con demasiada frecuencia en el resto del set. De tal manera que cada descripción se convertirá en un vector numérico.

# #### **Importación de librerías**

# In[91]:


import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion


# In[92]:


#variables a utilizar
X_train_movimiento
X_test_movimiento
y_train_movimiento
y_test_movimiento

X_train_categoria
X_test_categoria
y_train_categoria
y_test_categoria


# #### **Regla para evitar fuga de información**
# 
# El vectorizador debe aprender su vocabulario únicamente con entrenamiento.
# 
# Regla:
# X_train_tfidf = vectorizador.fit_transform(X_train)
# X_test_tfidf = vectorizador.transform(X_test)
# 

# #### **Primera prueba: TF-IDF de palabras**
# 
# 

# ##### **Versión inicial**

# In[93]:


tfidf_palabras_prueba = TfidfVectorizer(
    lowercase=False,
    strip_accents="unicode",
    analyzer="word",
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    norm="l2",
    dtype=np.float32
)


# ##### **Audita la primera configuración**

# In[94]:


#prueba en la tarea de tipo de movimiento
X_train_movimiento_prueba = (
    tfidf_palabras_prueba.fit_transform(
        X_train_movimiento
    )
)

X_test_movimiento_prueba = (
    tfidf_palabras_prueba.transform(
        X_test_movimiento
    )
)


# In[95]:


#revisa las dimensiones
print(
    "Train:",
    X_train_movimiento_prueba.shape
)

print(
    "Test:",
    X_test_movimiento_prueba.shape
)


#Cada fila es una transacción y cada columna una característica textual.


# ##### **Detectar vectores vacíos**
# 
# Una descripción genera un vector vacío cuando ninguno de sus términos existe en el vocabulario aprendido con entrenamiento.
# 

# In[96]:


vectores_vacios_train = (
    X_train_movimiento_prueba
    .getnnz(axis=1) == 0
).sum()

vectores_vacios_test = (
    X_test_movimiento_prueba
    .getnnz(axis=1) == 0
).sum()

print(
    "Vectores vacíos en train:",
    vectores_vacios_train
)

print(
    "Vectores vacíos en test:",
    vectores_vacios_test
)

print(
    "Porcentaje vacío en test:",
    round(
        vectores_vacios_test
        / X_test_movimiento_prueba.shape[0]
        * 100,
        2
    )
)


# Los resultados demuestran que el split contiene frases realmente nuevas y algunas están formadas completamente por palabras que no aparecen en entrenamiento.
# 
# Por ello se utilizará una representación híbrida.

# #### **Representación híbrida: palabras + caracteres**

# ##### **Crea función para construir el extractor**

# In[97]:


def crear_extractor_tfidf():
    """
    Combina TF-IDF de palabras y caracteres.

    La función crea un objeto nuevo cada vez para evitar
    compartir vocabulario entre las dos tareas.
    """

    tfidf_palabras = TfidfVectorizer(
        lowercase=False,
        strip_accents="unicode",
        analyzer="word",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
        norm="l2",
        dtype=np.float32
    )

    tfidf_caracteres = TfidfVectorizer(
        lowercase=False,
        strip_accents="unicode",
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_df=1.0,
        sublinear_tf=True,
        norm="l2",
        dtype=np.float32
    )

    extractor = FeatureUnion(
        transformer_list=[
            ("palabras", tfidf_palabras),
            ("caracteres", tfidf_caracteres)
        ],
        transformer_weights={
            "palabras": 1.0,
            "caracteres": 1.0
        }
    )

    return extractor


# char_wb crea fragmentos de caracteres dentro de los límites de cada palabra. Por ejemplo, a partir de la palabra pagué, puede extraer fragmentos como pag, pagu o ague. Este enfoque permite que el modelo identifique similitudes entre palabras que comparten una misma raíz o secuencias de caracteres, como pago, pagué, pagando y pagamos. Además, proporciona cierta tolerancia ante errores ortográficos o pequeñas variaciones en la escritura, lo que contribuye a que el modelo reconozca términos relacionados incluso cuando no están escritos exactamente de la misma manera.

# **Se utilizan configuraciones diferentes para las características basadas en palabras y en caracteres debido a la naturaleza de la información que genera cada representación.** En el caso de las palabras, se establece `min_df=1`, ya que, al contar con solo 428 descripciones únicas de entrenamiento en la primera tarea, una palabra que aparece pocas veces puede contener información relevante para la clasificación. Términos como `hipoteca`, `herencia`, `Netflix` o `Afore` podrían tener una frecuencia reducida dentro del conjunto de datos y, aun así, aportar señales importantes para identificar determinados tipos de movimientos. Por esta razón, se conservan incluso las palabras que aparecen una sola vez.
# 
# En el caso de las características basadas en caracteres, se utiliza `min_df=2`. Los fragmentos de caracteres generan una cantidad considerablemente mayor de características que las palabras, por lo que incluir aquellos que aparecen una sola vez podría incrementar innecesariamente el ruido y la dimensionalidad de la representación. Exigir que cada fragmento aparezca al menos dos veces permite controlar el tamaño del espacio de características y descartar patrones demasiado aislados, manteniendo aquellos que tienen mayor probabilidad de aportar información útil al modelo.
# 
# Por otra parte, no se eliminan las *stopwords*, ya que, aunque palabras como `de`, `la`, `para` o `me` suelen considerarse poco informativas de manera individual, pueden formar parte de expresiones relevantes cuando se trabaja con descripciones cortas. Frases como `pago de tarjeta`, `me cayó la nómina`, `para la escuela` o `de la renta` contienen estructuras lingüísticas que pueden ayudar a distinguir el contexto y significado de una transacción. Por ello, conservar estas palabras permite preservar información contextual que podría perderse si se aplicara una eliminación automática de *stopwords*.
# 

# ### **TF-IDF para tipo de movimiento** (TF-IDF híbrido + LinearSVC)

# In[98]:


#crea un extractor independiente
extractor_movimiento = crear_extractor_tfidf()


# In[99]:


#ajusta el extractor al entrenamiento
X_train_movimiento_tfidf = (
    extractor_movimiento.fit_transform(
        X_train_movimiento
    )
)


# In[100]:


#transforma prueba sin volver a ajustar
X_test_movimiento_tfidf = (
    extractor_movimiento.transform(
        X_test_movimiento
    )
)


# In[101]:


#revisa dimensiones
print(
    "Matriz train:",
    X_train_movimiento_tfidf.shape
)

print(
    "Matriz test:",
    X_test_movimiento_tfidf.shape
)


# Eso significa:
# 
# - 3,740 transacciones de entrenamiento.
# - 936 transacciones de prueba.
# - 5,419 características textuales.
# 
# Las columnas son exactamente las mismas en ambas matrices porque el vocabulario se aprendió solamente con entrenamiento.

# In[102]:


#separa vocabulario de palabras y caracteres
vectorizador_palabras_movimiento = (
    extractor_movimiento
    .transformer_list[0][1]
)

vectorizador_caracteres_movimiento = (
    extractor_movimiento
    .transformer_list[1][1]
)

numero_palabras_movimiento = len(
    vectorizador_palabras_movimiento
    .get_feature_names_out()
)

numero_caracteres_movimiento = len(
    vectorizador_caracteres_movimiento
    .get_feature_names_out()
)

print(
    "Características de palabras:",
    numero_palabras_movimiento
)

print(
    "Características de caracteres:",
    numero_caracteres_movimiento
)

print(
    "Total:",
    numero_palabras_movimiento
    + numero_caracteres_movimiento
)


# ##### **Inspección de características**
# 
# FeatureUnion agrega un prefijo para identificar el origen de cada característica

# In[103]:


nombres_features_movimiento = (
    extractor_movimiento
    .get_feature_names_out()
)

nombres_features_movimiento[:30]


#el resultado confirma que se están combinando ambos niveles de representación.


# ### **TF-IDF para categoría** (TF-IDF híbrido + regresión logística)

# In[104]:


#crea otro extractor diferente al anterior
extractor_categoria = crear_extractor_tfidf()



#el clasificador de categorías solo debe aprender vocabulario de transacciones de consumo.


# In[105]:


#ajusta el extractor
X_train_categoria_tfidf = (
    extractor_categoria.fit_transform(
        X_train_categoria
    )
)


# In[106]:


#transforma la prueba
X_test_categoria_tfidf = (
    extractor_categoria.transform(
        X_test_categoria
    )
)


# In[107]:


#revisa las dimensiones
print(
    "Matriz train:",
    X_train_categoria_tfidf.shape
)

print(
    "Matriz test:",
    X_test_categoria_tfidf.shape
)


# Tenemos:
# 
# - 3,316 consumos para entrenamiento.
# - 832 consumos para prueba.
# - 4,603 características textuales.

# ##### **Revisa el vocabulario de categorías**

# In[108]:


vectorizador_palabras_categoria = (
    extractor_categoria
    .transformer_list[0][1]
)

vectorizador_caracteres_categoria = (
    extractor_categoria
    .transformer_list[1][1]
)

numero_palabras_categoria = len(
    vectorizador_palabras_categoria
    .get_feature_names_out()
)

numero_caracteres_categoria = len(
    vectorizador_caracteres_categoria
    .get_feature_names_out()
)

print(
    "Características de palabras:",
    numero_palabras_categoria
)

print(
    "Características de caracteres:",
    numero_caracteres_categoria
)

print(
    "Total:",
    numero_palabras_categoria
    + numero_caracteres_categoria
)


# El vocabulario es menor porque esta tarea solo utiliza descripciones de consumo.

# ### **Auditoria de las matrices**

# In[109]:


#función de diagnóstico
def auditar_matriz_tfidf(
    matriz_train,
    matriz_test,
    nombre
):
    vacios_train = (
        matriz_train.getnnz(axis=1) == 0
    ).sum()

    vacios_test = (
        matriz_test.getnnz(axis=1) == 0
    ).sum()

    total_celdas = (
        matriz_train.shape[0]
        * matriz_train.shape[1]
    )

    densidad = (
        matriz_train.nnz
        / total_celdas
        * 100
    )

    memoria_bytes = (
        matriz_train.data.nbytes
        + matriz_train.indices.nbytes
        + matriz_train.indptr.nbytes
    )

    memoria_mb = memoria_bytes / (1024 ** 2)

    resumen = pd.Series({
        "tarea": nombre,
        "filas_train": matriz_train.shape[0],
        "filas_test": matriz_test.shape[0],
        "caracteristicas": matriz_train.shape[1],
        "valores_no_cero_train": matriz_train.nnz,
        "vectores_vacios_train": vacios_train,
        "vectores_vacios_test": vacios_test,
        "densidad_porcentaje": round(densidad, 4),
        "memoria_train_mb": round(memoria_mb, 3)
    })

    return resumen


# In[110]:


#aplica al set
auditoria_movimiento = auditar_matriz_tfidf(
    X_train_movimiento_tfidf,
    X_test_movimiento_tfidf,
    "Tipo de movimiento"
)

auditoria_categoria = auditar_matriz_tfidf(
    X_train_categoria_tfidf,
    X_test_categoria_tfidf,
    "Categoría"
)

auditoria_tfidf = pd.DataFrame([
    auditoria_movimiento,
    auditoria_categoria
])

auditoria_tfidf


# La combinación de palabras y caracteres eliminó los vectores vacíos.

# In[111]:


#Verifica que las matrices sigan siendo dispersas
from scipy.sparse import issparse

assert issparse(
    X_train_movimiento_tfidf
)

assert issparse(
    X_test_movimiento_tfidf
)

assert issparse(
    X_train_categoria_tfidf
)

assert issparse(
    X_test_categoria_tfidf
)

print("Todas las matrices conservan formato disperso.")


# ### **Validación final**

# In[112]:


from scipy.sparse import issparse

assert issparse(
    X_train_movimiento_tfidf
)

assert issparse(
    X_test_movimiento_tfidf
)

assert issparse(
    X_train_categoria_tfidf
)

assert issparse(
    X_test_categoria_tfidf
)

print("Todas las matrices conservan formato disperso.")


# ### **Conclusiones de la sección**
# 
# Las descripciones fueron representadas mediante una combinación de TF-IDF de palabras y n-gramas de caracteres. El componente de palabras utiliza unigramas y bigramas para capturar términos y expresiones completas, mientras que el componente de caracteres utiliza secuencias de tres a cinco caracteres para reconocer variantes morfológicas, conjugaciones y diferencias ortográficas.
# 
# Cada extractor fue ajustado exclusivamente sobre su correspondiente conjunto de entrenamiento. El conjunto de prueba fue transformado utilizando el vocabulario aprendido en entrenamiento, evitando así fuga de información.
# 
# Una representación inicial basada únicamente en palabras produjo vectores vacíos para 14.85% del conjunto de prueba de movimientos y 10.58% del conjunto de prueba de categorías. La representación híbrida eliminó por completo estos casos. La tarea de movimiento produjo 5,419 características y la tarea de categoría 4,603, conservando en ambos casos matrices dispersas con una densidad inferior al 1%.

# ## **Construcción, evaluación y serialización de pipelines**

# In[113]:


#importación de librerias
import joblib
import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.base import clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC


# In[114]:


#variables a utilizar
train_movimiento
test_movimiento

train_categoria
test_categoria


# #### **Crea el extractor TF-IDF**
# Aunque el entrenamiento utiliza descripcion_limpia, esto hará al pipeline más resistente cuando reciba texto directamente desde el backend.

# In[115]:


#crea el extractor TF-IDF
lowercase=True


# In[116]:


def crear_extractor_tfidf():

    tfidf_palabras = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        analyzer="word",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
        norm="l2",
        dtype=np.float32
    )

    tfidf_caracteres = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_df=1.0,
        sublinear_tf=True,
        norm="l2",
        dtype=np.float32
    )

    return FeatureUnion(
        transformer_list=[
            ("palabras", tfidf_palabras),
            ("caracteres", tfidf_caracteres)
        ],
        transformer_weights={
            "palabras": 1.0,
            "caracteres": 1.0
        }
    )


# #### **Definir los clasificadores candidatos**
# 
# Compara tres algoritmos adecuados para matrices dispersas de texto:

# In[117]:


#define los clasificadores candidatos
modelos_candidatos = {
    "Regresión logística": LogisticRegression(
        C=2.0,
        class_weight="balanced",
        max_iter=3000,
        solver="lbfgs",
        random_state=42
    ),

    "LinearSVC": LinearSVC(
        C=1.0,
        class_weight="balanced",
        random_state=42
    ),

    "ComplementNB": ComplementNB(
        alpha=0.5
    )
}


# Razón de cada candidato:
# - LogisticRegression: modelo lineal interpretable y con predict_proba.
# - LinearSVC: suele funcionar muy bien con texto y muchas características.
# - ComplementNB: baseline clásico para clasificación de texto desbalanceado.

# #### **Función para construir un pipeline**

# In[118]:


def crear_pipeline(clasificador):

    return Pipeline(
        steps=[
            (
                "tfidf",
                crear_extractor_tfidf()
            ),
            (
                "clasificador",
                clasificador
            )
        ]
    )


# ### **Comparación de modelos**
# 
# La selección se hará solamente dentro de train, mediante otra validación cruzada agrupada por descripcion_limpia.

# In[119]:


def evaluar_candidatos_cv(
    datos_train,
    columna_objetivo,
    modelos,
    n_splits=5,
    random_state=123
):
    cv = StratifiedGroupKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state
    )

    resultados = []

    X = datos_train["descripcion_limpia"]
    y = datos_train[columna_objetivo]
    grupos = datos_train["descripcion_limpia"]

    for nombre_modelo, clasificador in modelos.items():

        scores_macro = []
        scores_accuracy = []

        for train_idx, validacion_idx in cv.split(
            X=X,
            y=y,
            groups=grupos
        ):
            pipeline = crear_pipeline(
                clone(clasificador)
            )

            X_train_fold = X.iloc[train_idx]
            y_train_fold = y.iloc[train_idx]

            X_validacion_fold = X.iloc[validacion_idx]
            y_validacion_fold = y.iloc[validacion_idx]

            pipeline.fit(
                X_train_fold,
                y_train_fold
            )

            predicciones = pipeline.predict(
                X_validacion_fold
            )

            scores_macro.append(
                f1_score(
                    y_validacion_fold,
                    predicciones,
                    average="macro",
                    zero_division=0
                )
            )

            scores_accuracy.append(
                accuracy_score(
                    y_validacion_fold,
                    predicciones
                )
            )

        resultados.append({
            "modelo": nombre_modelo,
            "f1_macro_promedio": np.mean(scores_macro),
            "f1_macro_std": np.std(scores_macro),
            "accuracy_promedio": np.mean(scores_accuracy)
        })

    return (
        pd.DataFrame(resultados)
        .sort_values(
            "f1_macro_promedio",
            ascending=False
        )
        .reset_index(drop=True)
    )


#El vectorizador se encuentra dentro del pipeline, por lo que en cada fold aprende vocabulario exclusivamente de su porción de entrenamiento.


# #### **Comparación de modelos para tipo de movimiento**

# In[120]:


resultados_cv_movimiento = evaluar_candidatos_cv(
    datos_train=train_movimiento,
    columna_objetivo="tipo_movimiento",
    modelos=modelos_candidatos
)

resultados_cv_movimiento


# Usaremos LinearSVC

# #### **Comparación de modelos para categoría**

# In[121]:


resultados_cv_categoria = evaluar_candidatos_cv(
    datos_train=train_categoria,
    columna_objetivo="categoria",
    modelos=modelos_candidatos
)

resultados_cv_categoria


# Aunque ComplementNB obtuvo mayor accuracy que LinearSVC, elegimos regresión logística porque obtuvo el mejor macro F1.

# ### **Construcción de los modelos seleccionados**

# #### **Pipeline para tipo de movimiento**

# In[122]:


pipeline_movimiento = Pipeline(
    steps=[
        (
            "tfidf",
            crear_extractor_tfidf()
        ),
        (
            "clasificador",
            LinearSVC(
                C=1.0,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)


# #### **Entrena con todo el conjunto de entrenamiento:**

# In[123]:


pipeline_movimiento.fit(
    train_movimiento["descripcion_limpia"],
    train_movimiento["tipo_movimiento"]
)


# #### **Pipeline para categoría**

# In[124]:


pipeline_categoria = Pipeline(
    steps=[
        (
            "tfidf",
            crear_extractor_tfidf()
        ),
        (
            "clasificador",
            LogisticRegression(
                C=2.0,
                class_weight="balanced",
                max_iter=3000,
                solver="lbfgs",
                random_state=42
            )
        )
    ]
)


# #### **Entrena con todo el conjunto de entrenamiento:**

# In[125]:


pipeline_categoria.fit(
    train_categoria["descripcion_limpia"],
    train_categoria["categoria"]
)


# ## **Evaluación final sobre test**

# In[126]:


#genera predicciones
pred_movimiento = pipeline_movimiento.predict(
    test_movimiento["descripcion_limpia"]
)

pred_categoria = pipeline_categoria.predict(
    test_categoria["descripcion_limpia"]
)


# In[127]:


#función de evaluación
def calcular_metricas(y_real, y_predicha):

    return pd.Series({
        "accuracy": accuracy_score(
            y_real,
            y_predicha
        ),

        "balanced_accuracy": balanced_accuracy_score(
            y_real,
            y_predicha
        ),

        "f1_macro": f1_score(
            y_real,
            y_predicha,
            average="macro"
        ),

        "f1_weighted": f1_score(
            y_real,
            y_predicha,
            average="weighted"
        )
    })


# In[128]:


#aplica la función creada
metricas_movimiento = calcular_metricas(
    test_movimiento["tipo_movimiento"],
    pred_movimiento
)

metricas_categoria = calcular_metricas(
    test_categoria["categoria"],
    pred_categoria
)

metricas_finales = pd.DataFrame({
    "Tipo de movimiento": metricas_movimiento,
    "Categoría": metricas_categoria
}).T

metricas_finales.round(4)


# ####  **Reporte del clasificador de movimiento**

# In[129]:


print(
    classification_report(
        test_movimiento["tipo_movimiento"],
        pred_movimiento,
        digits=4,
        zero_division=0
    )
)


# El principal problema es la clase Ingreso.
# 
# De los 51 ingresos del test:
# 
# - 21 fueron clasificados correctamente.
# - 25 se confundieron con Consumo.
# - 5 se confundieron con Ahorro e inversión.

# ####  **Reporte del clasificador de categoría**

# In[130]:


print(
    classification_report(
        test_categoria["categoria"],
        pred_categoria,
        digits=4,
        zero_division=0
    )
)


# La categoría más problemática es Entretenimiento y ocio.
# 
# También existe una confusión importante entre: Alimentación → Vivienda. De 323 ejemplos reales de Alimentación, 75 fueron clasificados como Vivienda.

# # **Evaluación visual y análisis de errores**
# 
# Este bloque complementa las métricas agregadas con inspección visual y análisis
# de casos concretos. Todas las observaciones corresponden al conjunto de prueba
# agrupado, cuyas descripciones no aparecen en entrenamiento.
# 

# In[131]:


try:
    from IPython.display import display
except ImportError:
    display = print


def graficar_matriz_confusion(
    y_real,
    y_predicha,
    titulo,
    normalizar=False
):
    etiquetas = sorted(pd.Series(y_real).unique())
    normalizacion = "true" if normalizar else None

    matriz = confusion_matrix(
        y_real,
        y_predicha,
        labels=etiquetas,
        normalize=normalizacion
    )

    plt.figure(figsize=(11, 8))
    sns.heatmap(
        matriz,
        annot=True,
        fmt=".2f" if normalizar else "g",
        cmap="Blues",
        xticklabels=etiquetas,
        yticklabels=etiquetas
    )
    plt.title(titulo)
    plt.xlabel("Clase predicha")
    plt.ylabel("Clase real")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()


graficar_matriz_confusion(
    test_movimiento["tipo_movimiento"],
    pred_movimiento,
    "Matriz de confusión - tipo de movimiento"
)

graficar_matriz_confusion(
    test_categoria["categoria"],
    pred_categoria,
    "Matriz de confusión normalizada - categoría",
    normalizar=True
)


# ## **Ejemplos clasificados incorrectamente**
# 
# Las tablas siguientes permiten revisar descripciones concretas y detectar si
# los errores provienen de ambigüedad semántica, vocabulario insuficiente o
# etiquetas que requieren mayor contexto.
# 

# In[132]:


errores_movimiento = (
    test_movimiento.loc[
        test_movimiento["tipo_movimiento"].to_numpy()
        != pred_movimiento,
        ["descripcion", "descripcion_limpia", "tipo_movimiento"]
    ]
    .assign(prediccion=pred_movimiento[
        test_movimiento["tipo_movimiento"].to_numpy()
        != pred_movimiento
    ])
    .rename(columns={"tipo_movimiento": "clase_real"})
)

errores_categoria = (
    test_categoria.loc[
        test_categoria["categoria"].to_numpy()
        != pred_categoria,
        ["descripcion", "descripcion_limpia", "categoria"]
    ]
    .assign(prediccion=pred_categoria[
        test_categoria["categoria"].to_numpy()
        != pred_categoria
    ])
    .rename(columns={"categoria": "clase_real"})
)

print("Errores de tipo de movimiento:", len(errores_movimiento))
display(errores_movimiento.head(20))

print("Errores de categoría:", len(errores_categoria))
display(errores_categoria.head(20))


# ## **Análisis específico de la clase Ingreso**
# 
# En lugar de fijar cantidades manualmente, el análisis se calcula a partir de
# las predicciones vigentes. Así seguirá siendo correcto después de cambiar el
# split o reentrenar el modelo.
# 

# In[133]:


mascara_ingreso = (
    test_movimiento["tipo_movimiento"].to_numpy()
    == "Ingreso"
)

analisis_ingreso = (
    pd.Series(
        pred_movimiento[mascara_ingreso],
        name="clase_predicha"
    )
    .value_counts()
    .rename_axis("clase_predicha")
    .reset_index(name="cantidad")
)

analisis_ingreso["porcentaje"] = (
    analisis_ingreso["cantidad"]
    / max(mascara_ingreso.sum(), 1)
    * 100
).round(2)

display(analisis_ingreso)

errores_ingreso = errores_movimiento[
    errores_movimiento["clase_real"] == "Ingreso"
]

display(errores_ingreso.head(20))


# ## **Análisis de la confusión Alimentación → Vivienda**

# In[134]:


mascara_alimentacion_vivienda = (
    (test_categoria["categoria"].to_numpy() == "Alimentación")
    & (pred_categoria == "Vivienda")
)

confusion_alimentacion_vivienda = (
    test_categoria.loc[
        mascara_alimentacion_vivienda,
        ["descripcion", "descripcion_limpia", "monto", "tipo_pago"]
    ]
    .assign(
        clase_real="Alimentación",
        prediccion="Vivienda"
    )
)

print(
    "Casos Alimentación → Vivienda:",
    len(confusion_alimentacion_vivienda)
)

display(confusion_alimentacion_vivienda.head(30))


# ## **Palabras y fragmentos con mayor influencia por clase**
# 
# Los coeficientes positivos más altos muestran las características que empujan
# la predicción hacia cada clase. El prefijo `palabras__` identifica unigramas o
# bigramas y `caracteres__` identifica fragmentos de caracteres.
# 

# In[135]:


def obtener_caracteristicas_influyentes(
    pipeline,
    n_caracteristicas=15
):
    extractor = pipeline.named_steps["tfidf"]
    clasificador = pipeline.named_steps["clasificador"]

    nombres = extractor.get_feature_names_out()
    coeficientes = clasificador.coef_
    clases = clasificador.classes_

    filas = []

    for indice_clase, clase in enumerate(clases):
        indices = np.argsort(
            coeficientes[indice_clase]
        )[-n_caracteristicas:][::-1]

        for posicion, indice_feature in enumerate(indices, start=1):
            filas.append({
                "clase": clase,
                "posicion": posicion,
                "caracteristica": nombres[indice_feature],
                "coeficiente": coeficientes[
                    indice_clase,
                    indice_feature
                ]
            })

    return pd.DataFrame(filas)


influencia_movimiento = obtener_caracteristicas_influyentes(
    pipeline_movimiento
)

influencia_categoria = obtener_caracteristicas_influyentes(
    pipeline_categoria
)

display(influencia_movimiento)
display(influencia_categoria)


# # **Optimización controlada de hiperparámetros**
# 
# La búsqueda utiliza un conjunto pequeño y explícito de configuraciones. No se
# emplea el conjunto de prueba para seleccionar hiperparámetros: cada alternativa
# se evalúa exclusivamente dentro de `train` mediante `StratifiedGroupKFold`,
# manteniendo agrupadas las descripciones idénticas.
# 
# Para mantener controlado el costo computacional, se modifica un factor principal
# por configuración respecto a la base, en lugar de construir un producto
# cartesiano grande.
# 

# In[136]:


def crear_extractor_tfidf_configurable(configuracion):
    tfidf_palabras = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        analyzer="word",
        ngram_range=configuracion["ngram_palabras"],
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
        norm="l2",
        dtype=np.float32
    )

    tfidf_caracteres = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        analyzer="char_wb",
        ngram_range=configuracion["ngram_caracteres"],
        min_df=2,
        max_df=1.0,
        sublinear_tf=True,
        norm="l2",
        dtype=np.float32
    )

    return FeatureUnion(
        transformer_list=[
            ("palabras", tfidf_palabras),
            ("caracteres", tfidf_caracteres)
        ],
        transformer_weights={
            "palabras": configuracion["peso_palabras"],
            "caracteres": configuracion["peso_caracteres"]
        }
    )


def crear_pipeline_configurable(tarea, configuracion):
    if tarea == "movimiento":
        clasificador = LinearSVC(
            C=configuracion["C"],
            class_weight=configuracion["class_weight"],
            random_state=42
        )
    elif tarea == "categoria":
        clasificador = LogisticRegression(
            C=configuracion["C"],
            class_weight=configuracion["class_weight"],
            max_iter=3000,
            solver="lbfgs",
            random_state=42
        )
    else:
        raise ValueError("Tarea desconocida.")

    return Pipeline(
        steps=[
            (
                "tfidf",
                crear_extractor_tfidf_configurable(configuracion)
            ),
            ("clasificador", clasificador)
        ]
    )


# In[137]:


CONFIGURACION_BASE_MOVIMIENTO = {
    "nombre": "base",
    "C": 1.0,
    "peso_palabras": 1.0,
    "peso_caracteres": 1.0,
    "ngram_palabras": (1, 2),
    "ngram_caracteres": (3, 5),
    "class_weight": "balanced"
}

CONFIGURACION_BASE_CATEGORIA = {
    **CONFIGURACION_BASE_MOVIMIENTO,
    "C": 2.0
}


def variar(base, nombre, **cambios):
    configuracion = {**base, **cambios}
    configuracion["nombre"] = nombre
    return configuracion


configuraciones_movimiento = [
    CONFIGURACION_BASE_MOVIMIENTO,
    variar(CONFIGURACION_BASE_MOVIMIENTO, "C_0.5", C=0.5),
    variar(CONFIGURACION_BASE_MOVIMIENTO, "C_2.0", C=2.0),
    variar(CONFIGURACION_BASE_MOVIMIENTO, "mas_palabras", peso_palabras=1.5),
    variar(CONFIGURACION_BASE_MOVIMIENTO, "mas_caracteres", peso_caracteres=1.5),
    variar(CONFIGURACION_BASE_MOVIMIENTO, "solo_unigramas", ngram_palabras=(1, 1)),
    variar(CONFIGURACION_BASE_MOVIMIENTO, "char_2_5", ngram_caracteres=(2, 5)),
    variar(CONFIGURACION_BASE_MOVIMIENTO, "sin_balanceo", class_weight=None)
]

configuraciones_categoria = [
    CONFIGURACION_BASE_CATEGORIA,
    variar(CONFIGURACION_BASE_CATEGORIA, "C_1.0", C=1.0),
    variar(CONFIGURACION_BASE_CATEGORIA, "C_4.0", C=4.0),
    variar(CONFIGURACION_BASE_CATEGORIA, "mas_palabras", peso_palabras=1.5),
    variar(CONFIGURACION_BASE_CATEGORIA, "mas_caracteres", peso_caracteres=1.5),
    variar(CONFIGURACION_BASE_CATEGORIA, "solo_unigramas", ngram_palabras=(1, 1)),
    variar(CONFIGURACION_BASE_CATEGORIA, "char_2_5", ngram_caracteres=(2, 5)),
    variar(CONFIGURACION_BASE_CATEGORIA, "sin_balanceo", class_weight=None)
]


# In[138]:


def evaluar_configuraciones_agrupadas(
    datos_train,
    columna_objetivo,
    tarea,
    configuraciones,
    n_splits=5,
    random_state=123
):
    X = datos_train["descripcion_limpia"].reset_index(drop=True)
    y = datos_train[columna_objetivo].reset_index(drop=True)
    grupos = datos_train["descripcion_limpia"].reset_index(drop=True)

    resultados = []

    for configuracion in configuraciones:
        cv = StratifiedGroupKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=random_state
        )

        scores = []

        for indice_train, indice_validacion in cv.split(X, y, grupos):
            pipeline = crear_pipeline_configurable(
                tarea,
                configuracion
            )

            pipeline.fit(
                X.iloc[indice_train],
                y.iloc[indice_train]
            )

            prediccion = pipeline.predict(
                X.iloc[indice_validacion]
            )

            scores.append(
                f1_score(
                    y.iloc[indice_validacion],
                    prediccion,
                    average="macro",
                    zero_division=0
                )
            )

        resultados.append({
            "configuracion": configuracion["nombre"],
            "f1_macro_cv": np.mean(scores),
            "f1_macro_std": np.std(scores),
            "parametros": configuracion
        })

    return (
        pd.DataFrame(resultados)
        .sort_values("f1_macro_cv", ascending=False)
        .reset_index(drop=True)
    )


# ## **Búsqueda para tipo de movimiento**

# In[139]:


resultados_optimizacion_movimiento = (
    evaluar_configuraciones_agrupadas(
        datos_train=train_movimiento,
        columna_objetivo="tipo_movimiento",
        tarea="movimiento",
        configuraciones=configuraciones_movimiento
    )
)

display(
    resultados_optimizacion_movimiento[
        ["configuracion", "f1_macro_cv", "f1_macro_std"]
    ]
)


# ## **Búsqueda para categoría**

# In[140]:


resultados_optimizacion_categoria = (
    evaluar_configuraciones_agrupadas(
        datos_train=train_categoria,
        columna_objetivo="categoria",
        tarea="categoria",
        configuraciones=configuraciones_categoria
    )
)

display(
    resultados_optimizacion_categoria[
        ["configuracion", "f1_macro_cv", "f1_macro_std"]
    ]
)


# ## **Selección, reentrenamiento y evaluación final**
# 
# El pipeline actual solo se reemplaza cuando otra configuración supera el macro
# F1 de la configuración base en la validación cruzada de `train`. Después de la
# selección se ajusta con todo `train` y se evalúa una vez sobre `test`.
# 

# In[141]:


def seleccionar_configuracion(
    resultados,
    configuraciones
):
    puntuacion_base = resultados.loc[
        resultados["configuracion"] == "base",
        "f1_macro_cv"
    ].iloc[0]

    mejor_fila = resultados.iloc[0]
    mejora = mejor_fila["f1_macro_cv"] > puntuacion_base + 1e-6

    nombre_seleccionado = (
        mejor_fila["configuracion"]
        if mejora
        else "base"
    )

    configuracion = next(
        config
        for config in configuraciones
        if config["nombre"] == nombre_seleccionado
    )

    return configuracion, mejora, puntuacion_base


config_movimiento, mejora_movimiento, f1_base_movimiento = (
    seleccionar_configuracion(
        resultados_optimizacion_movimiento,
        configuraciones_movimiento
    )
)

config_categoria, mejora_categoria, f1_base_categoria = (
    seleccionar_configuracion(
        resultados_optimizacion_categoria,
        configuraciones_categoria
    )
)

pipeline_movimiento = crear_pipeline_configurable(
    "movimiento",
    config_movimiento
)
pipeline_movimiento.fit(
    train_movimiento["descripcion_limpia"],
    train_movimiento["tipo_movimiento"]
)

pipeline_categoria = crear_pipeline_configurable(
    "categoria",
    config_categoria
)
pipeline_categoria.fit(
    train_categoria["descripcion_limpia"],
    train_categoria["categoria"]
)

pred_movimiento = pipeline_movimiento.predict(
    test_movimiento["descripcion_limpia"]
)
pred_categoria = pipeline_categoria.predict(
    test_categoria["descripcion_limpia"]
)

metricas_movimiento = calcular_metricas(
    test_movimiento["tipo_movimiento"],
    pred_movimiento
)
metricas_categoria = calcular_metricas(
    test_categoria["categoria"],
    pred_categoria
)

metricas_finales_optimizadas = pd.DataFrame({
    "Tipo de movimiento": metricas_movimiento,
    "Categoría": metricas_categoria
}).T

resumen_seleccion = pd.DataFrame([
    {
        "tarea": "Tipo de movimiento",
        "configuracion": config_movimiento["nombre"],
        "reemplazo_la_base": mejora_movimiento,
        "f1_macro_cv_base": f1_base_movimiento,
        "f1_macro_test_final": metricas_movimiento["f1_macro"]
    },
    {
        "tarea": "Categoría",
        "configuracion": config_categoria["nombre"],
        "reemplazo_la_base": mejora_categoria,
        "f1_macro_cv_base": f1_base_categoria,
        "f1_macro_test_final": metricas_categoria["f1_macro"]
    }
])

display(resumen_seleccion)
display(metricas_finales_optimizadas.round(4))


# La decisión de reemplazo se basa exclusivamente en la validación
# cruzada agrupada dentro de entrenamiento. Las métricas de prueba se reportan
# como estimación final de generalización y no intervienen en la elección de
# hiperparámetros. Los objetos `pipeline_movimiento` y `pipeline_categoria` que
# continúan hacia la sección de serialización corresponden a las configuraciones
# seleccionadas.
# 

# ## **Serialización**

# #### **Guarda ambos pipelines completos**

# In[142]:


from pathlib import Path

directorio_modelos = Path("modelos")
directorio_modelos.mkdir(
    parents=True,
    exist_ok=True
)


# In[143]:


ruta_pipeline_movimiento = (
    directorio_modelos
    / "pipeline_tipo_movimiento.joblib"
)

ruta_pipeline_categoria = (
    directorio_modelos
    / "pipeline_categoria.joblib"
)

joblib.dump(
    pipeline_movimiento,
    ruta_pipeline_movimiento,
    compress=3
)

joblib.dump(
    pipeline_categoria,
    ruta_pipeline_categoria,
    compress=3
)


# Cada archivo contiene:
# TF-IDF de palabras
#         +
# TF-IDF de caracteres
#         +
# Clasificador entrenado
#         +
# Vocabulario
#         +
# Pesos aprendidos
#         +
# Nombres de las clases

# #### **Recarga de los pipelines**

# In[144]:


pipeline_movimiento_recargado = joblib.load(
    ruta_pipeline_movimiento
)

pipeline_categoria_recargado = joblib.load(
    ruta_pipeline_categoria
)


# #### **Verifica que la serialización no cambió predicciones**

# In[145]:


pred_movimiento_recargado = (
    pipeline_movimiento_recargado.predict(
        test_movimiento["descripcion_limpia"]
    )
)

pred_categoria_recargado = (
    pipeline_categoria_recargado.predict(
        test_categoria["descripcion_limpia"]
    )
)

assert np.array_equal(
    pred_movimiento,
    pred_movimiento_recargado
)

assert np.array_equal(
    pred_categoria,
    pred_categoria_recargado
)

print("Los pipelines recargados producen las mismas predicciones.")


# #### **Prueba con texto nuevo**

# In[146]:


#Tipo de movimiento

ejemplos_movimiento = [
    "ME CAYÓ LA NÓMINA",
    "Pagué todo lo de la tarjeta",
    "aparté dinero para ahorrar"
]

pipeline_movimiento_recargado.predict(
    ejemplos_movimiento
)


# In[147]:


#Categoría
ejemplos_categoria = [
    "compré comida para la semana",
    "pagué el camión",
    "fui al doctor"
]

pipeline_categoria_recargado.predict(
    ejemplos_categoria
)


# **Conclusión:** Se compararon tres algoritmos utilizando validación cruzada estratificada y agrupada dentro del conjunto de entrenamiento. La selección se realizó mediante macro F1 para considerar el desempeño de todas las clases, incluidas aquellas con menor representación.
# 
# LinearSVC obtuvo el mejor resultado para la clasificación del tipo de movimiento, mientras que la regresión logística obtuvo el mejor macro F1 para la clasificación de categorías. Ambos modelos fueron integrados con sus correspondientes extractores TF-IDF mediante objetos Pipeline.
# 
# Los pipelines completos fueron serializados con joblib y posteriormente recargados. Las predicciones obtenidas después de la recarga fueron idénticas a las originales, reduciendo el riesgo de inconsistencias entre el notebook de entrenamiento y el entorno de producción.

# # **Integración con motor financiero**
# 
# El contrato de entrada de la API contiene `usuario` (UUID y nombre), `periodo`,
# `ingresos` ya identificados y `transacciones` todavía sin clasificar.
# 
# El flujo de integración es:
# 
# 1. Validar el JSON de entrada.
# 2. Convertir únicamente `transacciones` a un DataFrame.
# 3. Clasificar tipo de movimiento y, cuando corresponda, categoría.
# 4. Conservar los ingresos recibidos y construir el diccionario clasificado.
# 5. Validar el contrato de salida antes de enviarlo al motor financiero.
# 

# ## **Importación y carga de modelos**

# In[148]:


import json
import joblib
import pandas as pd

from pathlib import Path
from uuid import UUID


# In[149]:


#carga de pipelines completos
pipeline_movimiento = joblib.load(
    "modelos/pipeline_tipo_movimiento.joblib"
)

pipeline_categoria = joblib.load(
    "modelos/pipeline_categoria.joblib"
)


# ## **Mapeo de categorías a grupos**

# In[150]:


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


# In[151]:


CLASIFICACIONES_VALIDAS = {
    "Consumo",
    "Pago de deuda",
    "Ahorro e inversión"
}

#Ingreso no aparece en transacciones, porque se mueve a la lista ingresos.


# ## **Validación y adaptación de la entrada de la API**
# 
# Estas funciones validan el contrato de entrada y convierten solamente la lista
# `transacciones` a la estructura tabular requerida por los clasificadores. Los
# ingresos ya identificados no vuelven a pasar por el modelo.
# 

# In[152]:


def convertir_fecha_iso(valor):
    return pd.to_datetime(
        valor,
        format="%Y-%m-%d",
        errors="raise"
    ).strftime("%Y-%m-%d")


def convertir_uuid(valor):
    """Valida y normaliza un identificador UUID."""
    try:
        return str(UUID(str(valor)))
    except (ValueError, TypeError, AttributeError) as error:
        raise ValueError(
            "usuario.id debe contener un UUID válido."
        ) from error


# In[153]:


def convertir_monto(valor):
    """Valida y convierte un monto a un tipo compatible con JSON."""
    monto = float(valor)

    if not pd.notna(monto) or monto <= 0:
        raise ValueError(
            "Todos los montos deben ser finitos y mayores que cero."
        )

    return round(monto, 2)


# In[154]:


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


# ## **Función principal de clasificación**
# 
# La función recibe el DataFrame creado a partir de `transacciones` y el JSON de
# entrada original. Conserva los ingresos recibidos y clasifica en lote las
# transacciones.
# 

# In[155]:


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


# ## **Validación del contrato de salida y función integradora**

# In[156]:


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


# ## **Aplicación al JSON recibido desde la API**

# ### **Ejemplo de entrada con UUID**

# In[157]:


datos_entrada = {
    "usuario": {
        "id": "8f7c2b91-3d64-4a12-9e58-71c6d8f204ab",
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
            "forma_pago": "Tarjeta de débito"
        },
        {
            "fecha": "2026-07-05",
            "descripcion": "Hospital Ángeles",
            "monto": 5800,
            "forma_pago": "Tarjeta de crédito",
            "tasa_de_interes_de_la_tarjeta": 48.5
        },
        {
            "fecha": "2026-07-08",
            "descripcion": "Pago préstamo personal",
            "monto": 3200,
            "forma_pago": "Transferencia bancaria"
        },
        {
            "fecha": "2026-07-12",
            "descripcion": "Netflix",
            "monto": 249,
            "forma_pago": "Tarjeta de crédito",
            "tasa_de_interes_de_la_tarjeta": 48.5
        },
        {
            "fecha": "2026-07-18",
            "descripcion": "Gasolina Pemex",
            "monto": 900,
            "forma_pago": "Efectivo"
        },
        {
            "fecha": "2026-07-22",
            "descripcion": "Aportación fondo de inversión",
            "monto": 2500,
            "forma_pago": "Transferencia bancaria"
        },
        {
            "fecha": "2026-07-26",
            "descripcion": "Liverpool",
            "monto": 4200,
            "forma_pago": "Tarjeta de crédito",
            "tasa_de_interes_de_la_tarjeta": 52.3
        }
    ]
}


# In[158]:


datos_clasificados = ejecutar_clasificacion(
    datos_entrada=datos_entrada,
    pipeline_movimiento=pipeline_movimiento,
    pipeline_categoria=pipeline_categoria
)


# In[159]:


print(
    json.dumps(
        datos_clasificados,
        ensure_ascii=False,
        allow_nan=False,
        indent=2
    )
)


# ### **Guarda el JSON clasificado**

# In[160]:


ruta_json = "datos_clasificados_ejemplo.json"

with open(ruta_json, "w", encoding="utf-8") as archivo:
    json.dump(
        datos_clasificados,
        archivo,
        ensure_ascii=False,
        allow_nan=False,
        indent=2
    )


# In[161]:


ruta_json


# # **Módulo perfiles financieros**

# # **Elaboración del Clasificador**

# In[162]:


df_clasificacion = df[
    df["tipo_movimiento"] == "Consumo"
].copy()


# --------------

# # **Implementación de motor financiero**

# ##  1.- Generación de constantes necesarias para el motor financiero

# In[163]:


# ============================================
# Categorías oficiales de consumo del sistema
# ============================================

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


# In[164]:


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


# In[165]:


PESOS_PERFIL_FINANCIERO = {

    "balance_financiero": 0.30,

    "capacidad_de_ahorro": 0.25,

    "endeudamiento": 0.25,

    "comportamiento_de_consumo": 0.20

}


# In[166]:


# ==========================================================
# Mapeo de categorías para la salida de la API
# ==========================================================

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


# ## 2.- Definición de función para obtener el estado de las dimensiones financieras y del perfil general

# In[167]:


def obtener_estado(puntuacion):

    if puntuacion >= 80:
        return "Saludable"

    elif puntuacion >= 50:
        return "En observación"

    else:
        return "En riesgo"


# ## 3.- Recepción de archivo JSON de prueba ya clasificado manualmente

# In[232]:


import json
import random
from pathlib import Path

def cargar_datos_clasificados(carpeta="datos"):
    """
    Selecciona aleatoriamente uno de los archivos JSON clasificados,
    lo convierte a un diccionario y lo devuelve.
    """

    carpeta_json = Path("perfiles_financieros_pruebas_clasificados_para_motor_financiero")

    numero = random.randint(1, 15)

    nombre_archivo = f"{numero:02d}_clasificado_manualmente.json"

    ruta_archivo = carpeta_json / nombre_archivo

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print(f"Archivo seleccionado: {nombre_archivo}")

    return datos


datos_clasificados_1 = cargar_datos_clasificados()
print (datos_clasificados_1)


# ## 4.- Generación de varibles globales

# In[169]:


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


# In[170]:


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


# In[171]:


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


# In[172]:


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


# In[173]:


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


# In[174]:


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


# In[175]:


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


# In[176]:


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


# In[177]:


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


# In[178]:


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


# In[179]:


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


# ## 5.- Generación de indicadores financieros por  cada una de las 4 dimenciones  

# In[180]:


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


# In[181]:


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


# In[182]:


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


# In[183]:


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


# In[184]:


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


# ## 6.- Obtención de la puntuación y estado de cada dimensión

# In[185]:


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


# In[186]:


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


# In[187]:


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


# In[188]:


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


# In[189]:


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


# ## 7.- Generación de recomendaciones de cada dimensión

# In[190]:


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


# In[191]:


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


# In[192]:


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


# In[193]:


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


# In[194]:


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


# ## 8.- Generacion de estado y puntuación del perfil financiero general

# In[195]:


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


# ## 9.- Generación de recomendacion general del perfil financiero

# In[196]:


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


# In[197]:


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


# In[198]:


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


# ## 10.- Construcción de diccionario final de entrega

# In[235]:


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


# ## 11.-Función maestra

# In[200]:


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


# ## 12 .- Verificación de la función maestra

# In[236]:


resultado_financiero = ejecutar_motor_financiero(
    datos_clasificados_1
)

import json

print(
    json.dumps(
        resultado_financiero,
        indent=4,
        ensure_ascii=False
    )
)


# # Función integradora de todo el modelo

# In[238]:


JSON_de_entrada_prueba={
  "usuario": {
    "id": "8f7c2b91-3d64-4a12-9e58-71c6d8f204ab",
    "nombre": "Nicolás Bravo"
  },
  "periodo": {
    "inicio": "2026-07-01",
    "fin": "2026-07-31"
  },
  "ingresos": [
    {
      "fecha": "2026-07-01",
      "descripcion": "Diseño de sitio web",
      "monto": 14000
    },
    {
      "fecha": "2026-07-02",
      "descripcion": "Proyecto de identidad visual",
      "monto": 9500
    },
    {
      "fecha": "2026-07-03",
      "descripcion": "Consultoría de marketing",
      "monto": 7000
    },
    {
      "fecha": "2026-07-04",
      "descripcion": "Venta de plantillas digitales",
      "monto": 3200
    }
  ],
  "transacciones": [
    {
      "fecha": "2026-07-02",
      "descripcion": "Renta departamento",
      "monto": 7500,
      "forma_pago": "Transferencia bancaria"
    },
    {
      "fecha": "2026-07-04",
      "descripcion": "Internet Totalplay",
      "monto": 699,
      "forma_pago": "Tarjeta de crédito",
      "tasa_de_interes_de_la_tarjeta": 58
    },
    {
      "fecha": "2026-07-05",
      "descripcion": "Adobe Creative Cloud",
      "monto": 899,
      "forma_pago": "Tarjeta de crédito",
      "tasa_de_interes_de_la_tarjeta": 58
    },
    {
      "fecha": "2026-07-06",
      "descripcion": "Google Workspace",
      "monto": 136,
      "forma_pago": "Tarjeta de crédito",
      "tasa_de_interes_de_la_tarjeta": 58
    },
    {
      "fecha": "2026-07-08",
      "descripcion": "Despensa Walmart",
      "monto": 2400,
      "forma_pago": "Tarjeta de débito"
    },
    {
      "fecha": "2026-07-10",
      "descripcion": "Gasolina Mobil",
      "monto": 1300,
      "forma_pago": "Tarjeta de débito"
    },
    {
      "fecha": "2026-07-12",
      "descripcion": "Pago provisional de impuestos SAT",
      "monto": 3200,
      "forma_pago": "Transferencia bancaria"
    },
    {
      "fecha": "2026-07-15",
      "descripcion": "Seguro de vida",
      "monto": 850,
      "forma_pago": "Transferencia bancaria"
    },
    {
      "fecha": "2026-07-18",
      "descripcion": "Fondo de inversión de deuda",
      "monto": 3500,
      "forma_pago": "Transferencia bancaria"
    },
    {
      "fecha": "2026-07-21",
      "descripcion": "Cuenta de ahorro para impuestos",
      "monto": 2500,
      "forma_pago": "Transferencia bancaria"
    },
    {
      "fecha": "2026-07-24",
      "descripcion": "Restaurante",
      "monto": 780,
      "forma_pago": "Tarjeta de crédito",
      "tasa_de_interes_de_la_tarjeta": 58
    },
    {
      "fecha": "2026-07-27",
      "descripcion": "Monitor para diseño",
      "monto": 4200,
      "forma_pago": "Tarjeta de crédito",
      "tasa_de_interes_de_la_tarjeta": 58
    },
    {
      "fecha": "2026-07-30",
      "descripcion": "Consulta médica",
      "monto": 750,
      "forma_pago": "Tarjeta de débito"
    }
  ]
}


# In[243]:


def funcion_integradora_final (datos):
	datos_clasificados = ejecutar_clasificacion(
    datos_entrada=datos,
    pipeline_movimiento=pipeline_movimiento,
    pipeline_categoria=pipeline_categoria
	)
	resultado_financiero = ejecutar_motor_financiero(datos_clasificados)
	return resultado_financiero


# In[244]:


resultado_final= funcion_integradora_final(JSON_de_entrada_prueba)

import json

print(
    json.dumps(
        resultado_final,
        indent=4,
        ensure_ascii=False
    )
)

