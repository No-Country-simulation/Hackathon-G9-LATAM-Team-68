package com.team68.finance_api.service;

import com.team68.finance_api.model.Medalla;
import com.team68.finance_api.model.TipoFinanciero;
import com.team68.finance_api.model.Transaccion;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.MedallaRepository;
import com.team68.finance_api.repository.TransaccionRepository;
import com.team68.finance_api.repository.UsuarioRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.*;

@Service
public class GamificacionService {

    private final UsuarioRepository usuarioRepository;
    private final TransaccionRepository transaccionRepository;
    private final MedallaRepository medallaRepository;

    public GamificacionService(UsuarioRepository usuarioRepository, 
                                TransaccionRepository transaccionRepository, 
                                MedallaRepository medallaRepository) {
        this.usuarioRepository = usuarioRepository;
        this.transaccionRepository = transaccionRepository;
        this.medallaRepository = medallaRepository;
    }

    @Transactional
    public void evaluarYAsignarMedallas(UUID usuarioId) {
        Usuario usuario = usuarioRepository.findByIdWithMedallas(usuarioId).orElse(null);
        if (usuario == null) return;

        List<Transaccion> transacciones = transaccionRepository.findByUsuarioId(usuarioId);
        List<Medalla> todasLasMedallas = medallaRepository.findAll();

        Set<String> codigosObtenidos = new HashSet<>();
        for (Medalla m : usuario.getMedallas()) {
            codigosObtenidos.add(m.getCodigo());
        }

        LocalDate hoy = LocalDate.now();

        for (Medalla medalla : todasLasMedallas) {
            if (codigosObtenidos.contains(medalla.getCodigo())) {
                continue;
            }

            boolean cumpleRequisito = false;

            switch (medalla.getCodigo()) {
                case "PEQUENO_OSEZNO":
                    cumpleRequisito = true;
                    break;

                case "PRIMERA_PRIMAVERA":
                    cumpleRequisito = verificarAntiguedad(transacciones, hoy, 30);
                    break;

                case "PREPARANDOTE_INVIERNO":
                    cumpleRequisito = verificarAntiguedad(transacciones, hoy, 180);
                    break;

                case "LETARGO_INVERNAL":
                    cumpleRequisito = verificarInactividad(transacciones, hoy, 30);
                    break;

                case "A_LA_GARRA_CREDITO":
                    cumpleRequisito = verificarBalanceMayorMesAnterior(transacciones, hoy);
                    break;

                case "RECOLECTOR_MIEL":
                    cumpleRequisito = verificarIngresosSemanalesSeguidos(transacciones, hoy, 3);
                    break;

                case "HIBERNACION_MONETARIA":
                    cumpleRequisito = verificarGastosNoSubieronMesAnterior(transacciones, hoy);
                    break;

                case "TREPANDO_CASCADA":
                    cumpleRequisito = verificarMejoraPorcentajeBalance(transacciones, hoy, new BigDecimal("0.25"));
                    break;

                case "SALMON_DORADO":
                    cumpleRequisito = verificarNumerosPositivosPrimerosDias(transacciones, hoy, 20);
                    break;
            }

            if (cumpleRequisito) {
                usuario.getMedallas().add(medalla);
            }
        }

        usuarioRepository.save(usuario);
    }

    private boolean verificarAntiguedad(List<Transaccion> transacciones, LocalDate hoy, long diasRequeridos) {
        return transacciones.stream()
                .filter(Objects::nonNull)
                .map(t -> t.getFecha())
                .filter(Objects::nonNull)
                .min((a, b) -> a.compareTo(b))
                .map(primeraFecha -> ChronoUnit.DAYS.between(primeraFecha, hoy) >= diasRequeridos)
                .orElse(false);
    }

    private boolean verificarInactividad(List<Transaccion> transacciones, LocalDate hoy, long diasInactivo) {
        return transacciones.stream()
                .filter(Objects::nonNull)
                .map(t -> t.getFecha())
                .filter(Objects::nonNull)
                .max((a, b) -> a.compareTo(b))
                .map(ultimaFecha -> ChronoUnit.DAYS.between(ultimaFecha, hoy) >= diasInactivo)
                .orElse(false);
    }

    private boolean verificarBalanceMayorMesAnterior(List<Transaccion> transacciones, LocalDate hoy) {
        LocalDate mesActualInicio = hoy.withDayOfMonth(1);
        LocalDate mesAnteriorInicio = mesActualInicio.minusMonths(1);
        LocalDate mesAnteriorFin = mesActualInicio.minusDays(1);

        BigDecimal balanceMesActual = calcularBalancePeriodo(transacciones, mesActualInicio, hoy);
        BigDecimal balanceMesAnterior = calcularBalancePeriodo(transacciones, mesAnteriorInicio, mesAnteriorFin);

        return balanceMesActual.compareTo(balanceMesAnterior) > 0;
    }

    private boolean verificarIngresosSemanalesSeguidos(List<Transaccion> transacciones, LocalDate hoy, int semanas) {
        for (int i = 0; i < semanas; i++) {
            LocalDate finSemana = hoy.minusWeeks(i);
            LocalDate inicioSemana = finSemana.minusDays(6);

            boolean tieneIngreso = transacciones.stream()
                    .filter(t -> t.getFecha() != null && !t.getFecha().isBefore(inicioSemana) && !t.getFecha().isAfter(finSemana))
                    .anyMatch(t -> esIngreso(t));

            if (!tieneIngreso) return false;
        }
        return true;
    }

    private boolean verificarGastosNoSubieronMesAnterior(List<Transaccion> transacciones, LocalDate hoy) {
        LocalDate mesActualInicio = hoy.withDayOfMonth(1);
        LocalDate mesAnteriorInicio = mesActualInicio.minusMonths(1);
        LocalDate mesAnteriorFin = mesActualInicio.minusDays(1);

        BigDecimal gastosMesActual = calcularGastosPeriodo(transacciones, mesActualInicio, hoy);
        BigDecimal gastosMesAnterior = calcularGastosPeriodo(transacciones, mesAnteriorInicio, mesAnteriorFin);

        return gastosMesActual.compareTo(gastosMesAnterior) <= 0;
    }

    private boolean verificarMejoraPorcentajeBalance(List<Transaccion> transacciones, LocalDate hoy, BigDecimal porcentaje) {
        LocalDate inicioMes = hoy.withDayOfMonth(1);
        BigDecimal balanceInicioMes = calcularBalancePeriodo(transacciones, inicioMes, inicioMes);
        BigDecimal balanceHoy = calcularBalancePeriodo(transacciones, inicioMes, hoy);

        if (balanceInicioMes.compareTo(BigDecimal.ZERO) <= 0) return false;

        BigDecimal incrementoRequerido = balanceInicioMes.multiply(BigDecimal.ONE.add(porcentaje));
        return balanceHoy.compareTo(incrementoRequerido) >= 0;
    }

    private boolean verificarNumerosPositivosPrimerosDias(List<Transaccion> transacciones, LocalDate hoy, int diasLimite) {
        if (hoy.getDayOfMonth() < diasLimite) return false;

        LocalDate inicioMes = hoy.withDayOfMonth(1);
        BigDecimal balanceAcumulado = BigDecimal.ZERO;

        for (int i = 1; i <= diasLimite; i++) {
            LocalDate dia = inicioMes.withDayOfMonth(i);
            BigDecimal balanceDia = calcularBalancePeriodo(transacciones, dia, dia);
            balanceAcumulado = balanceAcumulado.add(balanceDia);

            if (balanceAcumulado.compareTo(BigDecimal.ZERO) < 0) {
                return false;
            }
        }
        return true;
    }

    private BigDecimal calcularBalancePeriodo(List<Transaccion> transacciones, LocalDate inicio, LocalDate fin) {
        return transacciones.stream()
                .filter(Objects::nonNull)
                .filter(t -> t.getFecha() != null
                        && !t.getFecha().isBefore(inicio)
                        && !t.getFecha().isAfter(fin))
                .filter(t -> t.getMonto() != null)
                .map(t -> {
                    BigDecimal monto = t.getMonto().abs();
                    return esGasto(t) ? monto.negate() : monto;
                })
                .reduce(BigDecimal.ZERO, (subtotal, amount) -> subtotal.add(amount));
    }

    private BigDecimal calcularGastosPeriodo(List<Transaccion> transacciones, LocalDate inicio, LocalDate fin) {
        return transacciones.stream()
                .filter(Objects::nonNull)
                .filter(t -> t.getFecha() != null
                        && !t.getFecha().isBefore(inicio)
                        && !t.getFecha().isAfter(fin))
                .filter(this::esGasto)
                .map(t -> t.getMonto())
                .filter(Objects::nonNull)
                .map(monto -> monto.abs())
                .reduce(BigDecimal.ZERO, (subtotal, amount) -> subtotal.add(amount));
    }

    // Auxiliares para determinar si una transacción es ingreso o gasto/salida
    private boolean esGasto(Transaccion t) {
        if (t.getTipoFinanciero() == TipoFinanciero.CONSUMO || t.getTipoFinanciero() == TipoFinanciero.PAGO_DEUDA) {
            return true;
        }
        return t.getMonto() != null && t.getMonto().compareTo(BigDecimal.ZERO) < 0;
    }

    private boolean esIngreso(Transaccion t) {
        return !esGasto(t) && t.getMonto() != null && t.getMonto().compareTo(BigDecimal.ZERO) > 0;
    }
}