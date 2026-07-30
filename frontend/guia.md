# Guía de formularios y gráficas

## 1. Objetivo
Este documento explica cómo fluye la información en el proyecto:
- Desde los formularios de ingreso/gasto.
- Hasta el almacenamiento local.
- Y finalmente a las tablas y gráficas.

## 2. Archivos clave

### Formularios y datos
- `public/assets/js/forms-local.js`
  - Conecta botones de guardado de formularios.
  - Arma el objeto del movimiento y llama al módulo de datos.
  - Muestra mensajes de éxito/error (SweetAlert o `alert`).
- `public/assets/js/movements-local.js`
  - Es la capa de datos local.
  - Lee/escribe en `localStorage` con la clave `team68-movimientos`.
  - Filtra movimientos para historial y actualiza tablas/totales.

### Graficas
- `public/pages/history.html`
  - Construye 2 gráficas de barras (gastos por categoría e ingresos por categoría).
  - Reacciona a cambios de filtros y tema.
- `public/pages/perfil.html`
  - Calcula métricas (salud, deuda, ahorro).
  - Dibuja 3 gráficas tipo doughnut con Chart.js.

## 3. Flujo de formularios

```mermaid
flowchart TD
  A[Usuario llena formulario] --> B[Click en Guardar]
  B --> C[forms-local.js lee campos]
  C --> D[team68Movements.add(payload)]
  D --> E[Validación + normalización]
  E --> F[Guardar en localStorage]
  F --> G[Reset de formulario]
  G --> H[Mensaje de éxito]
  F --> I[Recarga de vistas/listas]
```

### 3.1 Captura de datos
En `forms-local.js` hay dos funciones principales:
- `setupIncomeForm()` para ingresos.
- `setupExpenseForm()` para gastos.

Ambas:
1. Buscan el formulario y botón (`saveIncomeBtn` o `saveExpenseBtn`).
2. En click, leen concepto, monto, fecha, categoría y cuenta/método.
3. Llaman a `window.team68Movements.add({...})`.

### 3.2 Validaciones
Las validaciones fuertes están en `movements-local.js`, dentro de `addMovement(payload)`:
- Concepto obligatorio.
- Fecha obligatoria.
- Monto numérico y mayor a 0.

Si algo falla, lanza `Error` y `forms-local.js` muestra mensaje de error.

### 3.3 Normalización del monto
`addMovement` ajusta signo segun tipo:
- `Ingreso` => monto positivo.
- `Gasto` => monto negativo.

Esto facilita cálculos de totales y gráficas.

### 3.4 Persistencia
Se guarda en `localStorage` bajo:
- `team68-movimientos`

Al iniciar, `ensureSeedData()` carga datos semilla si no hay registros.

## 4. Cómo se actualiza la vista tras guardar

Después de guardar, hay dos comportamientos:
- `forms-local.js` actualiza listas recientes (últimos ingresos/gastos).
- `movements-local.js` mantiene las vistas de resumen/historial con:
  - `loadSummaryTable()`
  - `loadHistoryTable()`

`loadHistoryTable()` además emite un evento:
- `team68:history-data-change`

Ese evento permite que las gráficas de historial se redibujen con los datos filtrados actuales.

## 5. Graficas en historial (`history.html`)

## 5.1 Origen de datos
1. Se obtiene `currentHistoryRows` desde filtros activos.
2. `getChartSeries(rows)` agrupa gastos por categoría.
3. `getIncomeChartSeries(rows)` agrupa ingresos por categoría.

Si no hay datos, se usa:
- Etiqueta: `Sin datos`
- Valor: `0`

## 5.2 Render de Chart.js
Se crean dos instancias tipo `bar`:
- `expenseCategoryChart`

Detalles importantes:
- Antes de crear una nueva grafica se hace `destroy()` de la anterior.
- `responsive: true` y `maintainAspectRatio: false`.
- Tooltip y eje Y formateados con prefijo `$`.

## 5.3 Re-render automático
Se redibujan cuando:
- Cambian datos del historial (`team68:history-data-change`).
- Cambia el tema (`team68:theme-change`).

## 6. Graficas de perfil financiero (`perfil.html`)

## 6.1 Cálculo de métricas
Con todos los movimientos:
- `income`: suma de ingresos.
- `expense`: suma de gastos absolutos.

Fórmulas:
- `debtPct = round((expense / income) * 100)`
- `savingsAmount = max(income - expense, 0)`
- `savingsPct = round((savingsAmount / income) * 100)`
- `healthPct = round(100 - debtPct * 0.6 + savingsPct * 0.4)`

Todo se limita a rango `[0, 100]`.

## 6.2 Dibujo de donuts
`drawDonut(canvasId, valueId, value, color)` crea cada grafica:
- Tipo `doughnut`.
- Dataset de 2 partes: `valor` y `resto`.
- Sin leyenda, con tooltip en porcentaje.

Se usa para:
- `saludChart`
- `deudaChart`
- `ahorroChart`

## 6.3 Estado y sugerencias
Según el porcentaje:
- Salud financiera: `saludable`, `en observación` o `en riesgo` (texto actual en código).
- Se llenan listas de sugerencias para salud, deuda y ahorro.

## 7. Resumen técnico rapido
- Los formularios no escriben directo en la UI final: delegan en `team68Movements`.
- `movements-local.js` centraliza reglas de negocio y persistencia.
- Las gráficas se alimentan de datos ya filtrados/normalizados.
- El evento `team68:history-data-change` desacopla tabla y gráficas en historial.

## 8. Recomendaciones de mantenimiento
- Mantener validaciones en un solo lugar (`addMovement`) para evitar inconsistencias.
- Si agregas nuevos tipos de movimiento, actualizar:
  - Normalización de monto.
  - Filtros de historial.
  - Serie de datos para charts.
- Para nuevos dashboards, reutilizar `getAll()` + funciones de agregación por categoría/periodo.

## 9. Contrato JSON para perfil financiero

La vista de perfil (`public/pages/perfil.html`) ahora acepta dos formatos:
- Formato nuevo (recomendado): claves simples en `camelCase`.
- Formato anterior: claves en `snake_case` (compatibilidad activa).

### 9.1 Formato recomendado

```json
{
  "user": {
    "id": 1,
    "name": "Brayan Lira"
  },
  "financialProfile": {
    "score": 76,
    "status": "En observacion"
  },
  "dimensions": {
    "financialBalance": {
      "score": 87,
      "status": "Saludable",
      "indicators": {
        "monthlyBalance": 5500,
        "expenseRate": 0.78,
        "financialMargin": 0.22
      },
      "recommendations": []
    },
    "savingsCapacity": {
      "score": 64,
      "status": "En observacion",
      "indicators": {
        "savingsRate": 0.08,
        "periodSavingsAndInvestment": 2000,
        "marginUsageRate": 0.36
      },
      "recommendations": []
    },
    "debt": {
      "score": 91,
      "status": "Saludable",
      "indicators": {
        "debtRatio": 0.12,
        "debtPaymentAmount": 3000,
        "debtPressure": 0.19,
        "averageDebtCost": 50.1
      },
      "recommendations": []
    },
    "consumptionBehavior": {
      "score": 58,
      "status": "En observacion",
      "indicators": {
        "expenseDistributionByCategory": {},
        "expenseConcentrationIndex": 0.58,
        "consumptionProfile": {
          "spendingPredominance": "Balance entre gastos esenciales y discrecionales",
          "consumptionType": "Moderadamente concentrado",
          "consumptionDiversification": "Diversificado",
          "mainCategory": "Vivienda"
        }
      },
      "recommendations": []
    }
  },
  "generalRecommendation": "Texto de recomendación general"
}
```

### 9.2 Entrada del payload en frontend

Se puede enviar de 2 formas:
- `window.team68FinancialPayload = {...}` antes de cargar la lógica de la página.
- `localStorage.setItem("team68-financial-profile", JSON.stringify(payload))`.

Si no existe payload, la página sigue calculando métricas locales con movimientos de `localStorage`.
