# Guia de formularios y graficas

## 1. Objetivo
Este documento explica como fluye la informacion en el proyecto:
- Desde los formularios de ingreso/gasto.
- Hasta el almacenamiento local.
- Y finalmente a las tablas y graficas.

## 2. Archivos clave

### Formularios y datos
- `public/assets/js/forms-local.js`
  - Conecta botones de guardado de formularios.
  - Arma el objeto del movimiento y llama al modulo de datos.
  - Muestra mensajes de exito/error (SweetAlert o `alert`).
- `public/assets/js/movements-local.js`
  - Es la capa de datos local.
  - Lee/escribe en `localStorage` con la clave `team68-movimientos`.
  - Filtra movimientos para historial y actualiza tablas/totales.

### Graficas
- `public/pages/history.html`
  - Construye 2 graficas de barras (gastos por categoria e ingresos por categoria).
  - Reacciona a cambios de filtros y tema.
- `public/pages/perfil.html`
  - Calcula metricas (salud, deuda, ahorro).
  - Dibuja 3 graficas tipo doughnut con Chart.js.

## 3. Flujo de formularios

```mermaid
flowchart TD
  A[Usuario llena formulario] --> B[Click en Guardar]
  B --> C[forms-local.js lee campos]
  C --> D[team68Movements.add(payload)]
  D --> E[Validacion + normalizacion]
  E --> F[Guardar en localStorage]
  F --> G[Reset de formulario]
  G --> H[Mensaje de exito]
  F --> I[Recarga de vistas/listas]
```

### 3.1 Captura de datos
En `forms-local.js` hay dos funciones principales:
- `setupIncomeForm()` para ingresos.
- `setupExpenseForm()` para gastos.

Ambas:
1. Buscan el formulario y boton (`saveIncomeBtn` o `saveExpenseBtn`).
2. En click, leen concepto, monto, fecha, categoria y cuenta/metodo.
3. Llaman a `window.team68Movements.add({...})`.

### 3.2 Validaciones
Las validaciones fuertes estan en `movements-local.js`, dentro de `addMovement(payload)`:
- Concepto obligatorio.
- Fecha obligatoria.
- Monto numerico y mayor a 0.

Si algo falla, lanza `Error` y `forms-local.js` muestra mensaje de error.

### 3.3 Normalizacion del monto
`addMovement` ajusta signo segun tipo:
- `Ingreso` => monto positivo.
- `Gasto` => monto negativo.

Esto facilita calculos de totales y graficas.

### 3.4 Persistencia
Se guarda en `localStorage` bajo:
- `team68-movimientos`

Al iniciar, `ensureSeedData()` carga datos semilla si no hay registros.

## 4. Como se actualiza la vista tras guardar

Despues de guardar, hay dos comportamientos:
- `forms-local.js` actualiza listas recientes (ultimos ingresos/gastos).
- `movements-local.js` mantiene las vistas de resumen/historial con:
  - `loadSummaryTable()`
  - `loadHistoryTable()`

`loadHistoryTable()` ademas emite un evento:
- `team68:history-data-change`

Ese evento permite que las graficas de historial se redibujen con los datos filtrados actuales.

## 5. Graficas en historial (`history.html`)

## 5.1 Origen de datos
1. Se obtiene `currentHistoryRows` desde filtros activos.
2. `getChartSeries(rows)` agrupa gastos por categoria.
3. `getIncomeChartSeries(rows)` agrupa ingresos por categoria.

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

## 5.3 Re-render automatico
Se redibujan cuando:
- Cambian datos del historial (`team68:history-data-change`).
- Cambia el tema (`team68:theme-change`).

## 6. Graficas de perfil financiero (`perfil.html`)

## 6.1 Calculo de metricas
Con todos los movimientos:
- `income`: suma de ingresos.
- `expense`: suma de gastos absolutos.

Formulas:
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
Segun el porcentaje:
- Salud financiera: `saludable`, `en observacion` o `en riego` (texto actual en codigo).
- Se llenan listas de sugerencias para salud, deuda y ahorro.

## 7. Resumen tecnico rapido
- Los formularios no escriben directo en la UI final: delegan en `team68Movements`.
- `movements-local.js` centraliza reglas de negocio y persistencia.
- Las graficas se alimentan de datos ya filtrados/normalizados.
- El evento `team68:history-data-change` desacopla tabla y graficas en historial.

## 8. Recomendaciones de mantenimiento
- Mantener validaciones en un solo lugar (`addMovement`) para evitar inconsistencias.
- Si agregas nuevos tipos de movimiento, actualizar:
  - Normalizacion de monto.
  - Filtros de historial.
  - Serie de datos para charts.
- Para nuevos dashboards, reutilizar `getAll()` + funciones de agregacion por categoria/periodo.
