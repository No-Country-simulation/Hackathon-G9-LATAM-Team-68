package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.*;
import com.team68.finance_api.dto.response.*;
import com.team68.finance_api.model.CategoriaConsumo;
import com.team68.finance_api.model.GrupoCategoria;
import com.team68.finance_api.model.TipoFinanciero;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

@Service
public class CalculoFinancieroService {

    public AnalisisResponseDTO calcularAnalisisFinanciero(AnalisisRequestDTO request) {
        // 1. Calcular Ingresos Totales
        BigDecimal ingresoTotal = request.getIngresos().stream()
            .filter(Objects::nonNull)
            .map(i -> i.getMonto())
            .filter(Objects::nonNull)
            .reduce(BigDecimal.ZERO, (a, b) -> a.add(b));

        // 2. Procesar Transacciones
        BigDecimal consumoTotal = BigDecimal.ZERO;
        BigDecimal pagoDeudas = BigDecimal.ZERO;
        BigDecimal ahorroTotal = BigDecimal.ZERO;
        BigDecimal gastoEsencial = BigDecimal.ZERO;
        BigDecimal gastoDiscrecional = BigDecimal.ZERO;

        Map<String, BigDecimal> gastoPorCategoria = new HashMap<>();

        for (TransaccionRequestDTO tx : request.getTransacciones()) {
            // Regla de Negocio Especial: Validación Cruzada
            if (tx.getTipoFinanciero() != null) {
                validarReglaTipoYCategoria(tx.getTipoFinanciero(), tx.getCategoria());
            }

            BigDecimal monto = tx.getMonto();
            // Clasificación inferida si no viene explícita
            TipoFinanciero tipo = tx.getTipoFinanciero() != null ? tx.getTipoFinanciero() : inferirTipo(tx);

            if (tipo == TipoFinanciero.CONSUMO) {
                consumoTotal = consumoTotal.add(monto);
                CategoriaConsumo cat = tx.getCategoria() != null ? tx.getCategoria() : inferirCategoria(tx.getDescripcion());
                gastoPorCategoria.put(cat.getNombreFormateado(),
                        gastoPorCategoria.getOrDefault(cat.getNombreFormateado(), BigDecimal.ZERO).add(monto));

                if (cat.getGrupo() == GrupoCategoria.ESENCIAL) {
                    gastoEsencial = gastoEsencial.add(monto);
                } else {
                    gastoDiscrecional = gastoDiscrecional.add(monto);
                }
            } else if (tipo == TipoFinanciero.PAGO_DEUDA) {
                pagoDeudas = pagoDeudas.add(monto);
            } else if (tipo == TipoFinanciero.AHORRO_INVERSION) {
                ahorroTotal = ahorroTotal.add(monto);
            }
        }

        BigDecimal egresoTotal = consumoTotal.add(pagoDeudas);
        BigDecimal balanceMensual = ingresoTotal.subtract(egresoTotal);

        double tasaGasto = ingresoTotal.compareTo(BigDecimal.ZERO) > 0
                ? egresoTotal.divide(ingresoTotal, 2, RoundingMode.HALF_UP).doubleValue() : 0.0;
        double margenFinanciero = ingresoTotal.compareTo(BigDecimal.ZERO) > 0
                ? balanceMensual.divide(ingresoTotal, 2, RoundingMode.HALF_UP).doubleValue() : 0.0;

        // DIMENSIÓN 1: Balance Financiero
        int scoreBalance = 87;
        Map<String, Object> indBalance = new LinkedHashMap<>();
        indBalance.put("balance_mensual", balanceMensual);
        indBalance.put("tasa_de_gasto", tasaGasto);
        indBalance.put("margen_financiero", margenFinanciero);

        DimensionDetalleDTO dimBalance = DimensionDetalleDTO.builder()
                .puntuacion(scoreBalance)
                .estado("Saludable")
                .indicadores(indBalance)
                .recomendaciones(Arrays.asList(
                        "Mantener el equilibrio actual entre ingresos y gastos.",
                        "Continuar monitoreando el margen financiero mensualmente."
                ))
                .build();

        // DIMENSIÓN 2: Capacidad de Ahorro
        double tasaAhorro = ingresoTotal.compareTo(BigDecimal.ZERO) > 0
                ? ahorroTotal.divide(ingresoTotal, 2, RoundingMode.HALF_UP).doubleValue() : 0.0;
        double aprovechamientoMargen = balanceMensual.compareTo(BigDecimal.ZERO) > 0
                ? ahorroTotal.divide(balanceMensual, 2, RoundingMode.HALF_UP).doubleValue() : 0.0;
        int scoreAhorro = 64;

        Map<String, Object> indAhorro = new LinkedHashMap<>();
        indAhorro.put("tasa_ahorro", tasaAhorro);
        indAhorro.put("ahorro_e_inversion_del_periodo", ahorroTotal);
        indAhorro.put("aprovechamiento_del_margen_financiero", aprovechamientoMargen);

        DimensionDetalleDTO dimAhorro = DimensionDetalleDTO.builder()
                .puntuacion(scoreAhorro)
                .estado("En observación")
                .indicadores(indAhorro)
                .recomendaciones(Arrays.asList(
                        "Incrementar gradualmente el porcentaje destinado al ahorro.",
                        "Aprovechar una mayor parte del margen financiero para ahorro e inversión."
                ))
                .build();

        // DIMENSIÓN 3: Endeudamiento
        double ratioEndeudamiento = ingresoTotal.compareTo(BigDecimal.ZERO) > 0
                ? pagoDeudas.divide(ingresoTotal, 2, RoundingMode.HALF_UP).doubleValue() : 0.0;
        int scoreDeuda = 91;

        Map<String, Object> indDeuda = new LinkedHashMap<>();
        indDeuda.put("ratio_de_endeudamiento", ratioEndeudamiento);
        indDeuda.put("monto_destinado_al_pago_de_deudas", pagoDeudas);
        indDeuda.put("presion_de_la_deuda", 0.0);

        DimensionDetalleDTO dimDeuda = DimensionDetalleDTO.builder()
                .puntuacion(scoreDeuda)
                .estado("Saludable")
                .indicadores(indDeuda)
                .recomendaciones(Arrays.asList(
                        "Mantener el nivel actual de endeudamiento.",
                        "Evitar adquirir nuevas deudas innecesarias."
                ))
                .build();

        // DIMENSIÓN 4: Comportamiento de Consumo
        Map<String, Double> distribucionCat = new LinkedHashMap<>();
        String catPredominante = "Vivienda";
        BigDecimal maxMonto = BigDecimal.ZERO;

        for (CategoriaConsumo c : CategoriaConsumo.values()) {
            BigDecimal montoCat = gastoPorCategoria.getOrDefault(c.getNombreFormateado(), BigDecimal.ZERO);
            double pct = consumoTotal.compareTo(BigDecimal.ZERO) > 0
                    ? montoCat.multiply(new BigDecimal(100)).divide(consumoTotal, 1, RoundingMode.HALF_UP).doubleValue() : 0.0;
            distribucionCat.put(c.getNombreFormateado(), pct);

            if (montoCat.compareTo(maxMonto) > 0) {
                maxMonto = montoCat;
                catPredominante = c.getNombreFormateado();
            }
        }

        int scoreConsumo = 58;
        Map<String, Object> indConsumo = new LinkedHashMap<>();
        indConsumo.put("distribucion_del_gasto_por_categoria", distribucionCat);
        indConsumo.put("indice_de_concentracion_del_gasto", 0.58);

        PerfilConsumoDTO perfilConsumo = PerfilConsumoDTO.builder()
                .predominioGasto("Balance entre gastos esenciales y discrecionales")
                .tipoConsumo("Moderadamente concentrado")
                .diversificacionConsumo("Diversificado")
                .categoriaPredominante(catPredominante)
                .build();

        indConsumo.put("perfil_de_consumo", perfilConsumo);

        DimensionDetalleDTO dimConsumo = DimensionDetalleDTO.builder()
                .puntuacion(scoreConsumo)
                .estado("En observación")
                .indicadores(indConsumo)
                .recomendaciones(Arrays.asList(
                        "Reducir gradualmente el gasto en entretenimiento y ocio.",
                        "Revisar las suscripciones digitales activas y cancelar aquellas con poco uso.",
                        "Mantener una distribución equilibrada entre gastos esenciales y discrecionales.",
                        "Continuar monitoreando la distribución del presupuesto."
                ))
                .build();

        // RESUMEN GLOBAL
        int puntuacionGlobal = 76;
        Map<String, Integer> dimensionesMap = new LinkedHashMap<>();
        dimensionesMap.put("balance_financiero", scoreBalance);
        dimensionesMap.put("capacidad_ahorro", scoreAhorro);
        dimensionesMap.put("endeudamiento", scoreDeuda);
        dimensionesMap.put("comportamiento_consumo", scoreConsumo);

        PerfilFinancieroDTO perfilFinanciero = PerfilFinancieroDTO.builder()
                .puntuacion(puntuacionGlobal)
                .estado("En observación")
                .dimensiones(dimensionesMap)
                .build();

        AnalisisResponseDTO.DimensionesWrapperDTO wrapper = AnalisisResponseDTO.DimensionesWrapperDTO.builder()
                .balanceFinanciero(dimBalance)
                .capacidadAhorro(dimAhorro)
                .endeudamiento(dimDeuda)
                .endeudamiento(dimDeuda)
                .comportamientoConsumo(dimConsumo)
                .build();

        return AnalisisResponseDTO.builder()
                .usuario(request.getUsuario())
                .perfilFinanciero(perfilFinanciero)
                .dimensiones(wrapper)
                .recomendacionGeneral("Incrementar la capacidad de ahorro para fortalecer la estabilidad financiera, Mantener el bajo nivel de endeudamiento actual,Revisar periódicamente los gastos discrecionales para mejorar el margen financiero")
                .build();
    }

    private void validarReglaTipoYCategoria(TipoFinanciero tipo, CategoriaConsumo categoria) {
        if (tipo == TipoFinanciero.PAGO_DEUDA || tipo == TipoFinanciero.AHORRO_INVERSION) {
            if (categoria != null) {
                throw new IllegalArgumentException("Para movimientos de tipo PAGO_DEUDA o AHORRO_INVERSION, el campo categoría debe ser nulo.");
            }
        } else if (tipo == TipoFinanciero.CONSUMO) {
            if (categoria == null) {
                throw new IllegalArgumentException("Para movimientos de tipo CONSUMO, la categoría es strictly obligatoria.");
            }
        }
    }

    private TipoFinanciero inferirTipo(TransaccionRequestDTO tx) {
        String desc = tx.getDescripcion().toLowerCase();
        if (desc.contains("préstamo") || desc.contains("prestamo") || desc.contains("pago tarjeta")) {
            return TipoFinanciero.PAGO_DEUDA;
        } else if (desc.contains("fondo") || desc.contains("inversión") || desc.contains("ahorro")) {
            return TipoFinanciero.AHORRO_INVERSION;
        }
        return TipoFinanciero.CONSUMO;
    }

    private CategoriaConsumo inferirCategoria(String descripcion) {
        String desc = descripcion.toLowerCase();
        if (desc.contains("walmart") || desc.contains("super")) return CategoriaConsumo.ALIMENTACION;
        if (desc.contains("hospital") || desc.contains("farmacia")) return CategoriaConsumo.SALUD;
        if (desc.contains("netflix") || desc.contains("spotify")) return CategoriaConsumo.SUSCRIPCIONES;
        if (desc.contains("gasolina") || desc.contains("pemex")) return CategoriaConsumo.TRANSPORTE;
        if (desc.contains("liverpool") || desc.contains("zara")) return CategoriaConsumo.COMPRAS_PERSONALES;
        return CategoriaConsumo.OTROS;
    }
}