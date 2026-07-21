# Propuestas para definición del sistema.

# Objetivo:
Reunir propuestas para complementar el modelo del sistema de evaluación de bienestar financiero bajo la perspectiva de la Ciencia de Datos.

---

# 1. Incorporar un sistema de puntuación (Financial Health Score)

Actualmente se clasifica el estado financiero en tres categorías:

- Saludable
- En observación
- En riesgo

Se propone complementar esta clasificación con un **Financial Health Score** en una escala de **0 a 100**. Lo cual permitirá medir la evolución del usuario a lo largo del tiempo, facilitará la construcción de dashboards, hará más intuitiva la interpretación del estado financiero y permitirá generar objetivos de mejora.


# 2. Delimitar los pesos para cada dimensión y definir los umbrales cuantitativos

Debido a que no todos los factores tienen el mismo impacto sobre el bienestar financiero, se recomienda asignar ponderaciones relativas a cada dimensión (Enduedamiento, Ahorros, Comportamiento de consumo), basándonos en literatura especializada para mayor asertividad y veracidad. Así mismo, definir un porcentaje de ahorro adecuado, qué nivel de endeudamiento se considera de riesgo, la cantidad de dinero que es sana para destinar a gastos diarios.

## Fuentes de consulta confiables: 

- OCDE
- Banco Mundial
- CONDUSEF
- FCA (Financial Conduct Authority)
- CFPB (Consumer Financial Protection Bureau)


# 3. Contextualizar el comportamiento de consumo

Se propone evaluar el consumo considerando:

- porcentaje respecto al ingreso;
- capacidad de ahorro;
- nivel de endeudamiento;
- balance financiero general.

De esta forma, la interpretación será más consistente y adaptada al contexto de cada usuario.


# 4. Definir estabilidad del ingreso

## Variables sugeridas

- Tipo de ingreso (fijo o variable)
- Frecuencia de ingreso
- Antigüedad laboral
- Estabilidad laboral

Estas variables permitirán distinguir entre usuarios con ingresos constantes y usuarios con ingresos fluctuantes, mejorando la interpretación y personalización del perfil financiero.


# 5. Incorporar una dimensión de resiliencia financiera

Esta dimensión busca recopilar información acerca de los fondos de emergencia del usuario, si posee uno o está construyendo uno, cuáto tiempo podría mantenerse con ese fondo o, incluso si sería capaz de solventar alguna enfermedad o imprevisto con ese dinero.

Esta información complementa el análisis tradicional basado únicamente en ingresos, ahorro y endeudamiento, proporcionando una visión más integral de la salud financiera.

---

# Propuesta metodológica para combinar el perfil financiero y Machine Learning


### Motor de perfil financiero

Responsable de calcular indicadores financieros como:

- Balance financiero
- Tasa de ahorro
- Ratio de endeudamiento
- Distribución del gasto
- Otros indicadores financieros

Este componente proporciona transparencia y facilita explicar al usuario cómo se obtuvo el resultado.


### Modelo de Machine Learning

Utilizar modelos supervisados para:

- Clasificar automáticamente las transacciones a partir de su descripción.
- Predecir el perfil financiero utilizando como variables de entrada los indicadores previamente calculados.

Esto permitirá capturar patrones complejos que difícilmente podrían representarse únicamente mediante reglas.


## Motor de recomendaciones

Finalmente, el sistema puede combinar:

- indicadores financieros;
- reglas de negocio;
- predicción del modelo de Machine Learning.

Con esta información se generan recomendaciones personalizadas y justificadas para cada usuario.

---

# Arquitectura propuesta

```text
Información financiera
            │
            ▼
Clasificación automática de transacciones
            │
            ▼
Cálculo de indicadores financieros
            │
            ▼
Motor de perfil financiero
            │
            ▼
Modelo de Machine Learning
            │
            ▼
Perfil financiero + Financial Health Score
            │
            ▼
Motor de recomendaciones personalizadas
```

Este enfoque aprovecha las fortalezas de ambos paradigmas: un sistema transparente y explicable mediante el modelo de perfiles financieros, complementado por modelos de aprendizaje automático capaces de identificar patrones complejos y mejorar la capacidad predictiva del sistema.