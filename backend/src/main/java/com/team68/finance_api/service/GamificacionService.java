package com.team68.finance_api.service;

import com.team68.finance_api.model.Ingreso;
import com.team68.finance_api.model.Medalla;
import com.team68.finance_api.model.Transaccion;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.IngresoRepository;
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
    private final IngresoRepository ingresoRepository;
    private final MedallaRepository medallaRepository;

    public GamificacionService(UsuarioRepository usuarioRepository,
                                TransaccionRepository transaccionRepository,
                                IngresoRepository ingresoRepository,
                                MedallaRepository medallaRepository) {
        this.usuarioRepository = usuarioRepository;
        this.transaccionRepository = transaccionRepository;
        this.ingresoRepository = ingresoRepository;
        this.medallaRepository = medallaRepository;
    }

    @Transactional
    public void evaluarYAsignarMedallas(UUID usuarioId) {
        Usuario usuario = usuarioRepository.findByIdWithMedallas(usuarioId).orElse(null);
        if (usuario == null) return;

        List<Transaccion> transacciones = transaccionRepository.findByUsuarioId(usuarioId);
        List<Ingreso> ingresos = ingresoRepository.findByUsuarioId(usuarioId);
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
                    cumpleRequisito = verificarAntiguedad(transacciones, ingresos, hoy, 30);
                    break;

                case "PREPARANDOTE_INVIERNO":
                    cumpleRequisito = verificarAntiguedad(transacciones, ingresos, hoy, 180);
                    break;

                case "LETARGO_INVERNAL":
                    cumpleRequisito = verificarInactividad(transacciones, ingresos, hoy, 30);
                    break;

                case "A_LA_GARRA_CREDITO":
                    cumpleRequisito = verificarBalanceMayorMesAnterior(transacciones, ingresos, hoy);
                    break;

                case "RECOLECTOR_MIEL":
                    cumpleRequisito = verificarIngresosSemanalesSeguidos(ingresos, hoy, 3);
                    break;

                case "HIBERNACION_MONETARIA":
                    cumpleRequisito = verificarGastosNoSubieronMesAnterior(transacciones, hoy);
                    break;

                case "TREPANDO_CASCADA":
                    cumpleRequisito = verificarMejoraPorcentajeBalance(transacciones, ingresos, hoy, new BigDecimal("0.25"));
                    break;

                case "SALMON_DORADO":
                    cumpleRequisito = verificarNumerosPositivosPrimerosDias(transacciones, ingresos, hoy, 20);
                    break;
            }

            if (cumpleRequisito) {
                usuario.getMedallas().add(medalla);
            }
        }

        usuarioRepository.save(usuario);
    }

    private boolean verificarAntiguedad(List<Transaccion> transacciones, List<Ingreso> ingresos, LocalDate hoy, long diasRequeridos) {
        Optional<LocalDate> primeraTransaccion = transacciones.stream()
                .filter(Objects::nonNull)
                .map(t -> t.getFecha())
                .filter(Objects::nonNull)
                .min((a, b) -> a.compareTo(b));

        Optional<LocalDate> primerIngreso = ingresos.stream()
                .filter(Objects::nonNull)
                .map(t -> t.getFecha())
                .filter(Objects::nonNull)
                .min((a, b) -> a.compareTo(b));

        LocalDate primeraFecha = null;
        if (primeraTransaccion.isPresent() && primerIngreso.isPresent()) {
            primeraFecha = primeraTransaccion.get().isBefore(primerIngreso.get()) ? primeraTransaccion.get() : primerIngreso.get();
        } else if (primeraTransaccion.isPresent()) {
            primeraFecha = primeraTransaccion.get();
        } else if (primerIngreso.isPresent()) {
            primeraFecha = primerIngreso.get();
        }

        return primeraFecha != null && ChronoUnit.DAYS.between(primeraFecha, hoy) >= diasRequeridos;
    }

    private boolean verificarInactividad(List<Transaccion> transacciones, List<Ingreso> ingresos, LocalDate hoy, long diasInactivo) {
        Optional<LocalDate> ultimaTransaccion = transacciones.stream()
                .filter(Objects::nonNull)
                .map(t -> t.getFecha())
                .filter(Objects::nonNull)
                .max((a, b) -> a.compareTo(b));

        Optional<LocalDate> ultimoIngreso = ingresos.stream()
                .filter(Objects::nonNull)
                .map(t -> t.getFecha())
                .filter(Objects::nonNull)
                .max((a, b) -> a.compareTo(b));

        LocalDate ultimaFecha = null;
        if (ultimaTransaccion.isPresent() && ultimoIngreso.isPresent()) {
            ultimaFecha = ultimaTransaccion.get().isAfter(ultimoIngreso.get()) ? ultimaTransaccion.get() : ultimoIngreso.get();
        } else if (ultimaTransaccion.isPresent()) {
            ultimaFecha = ultimaTransaccion.get();
        } else if (ultimoIngreso.isPresent()) {
            ultimaFecha = ultimoIngreso.get();
        }
        return ultimaFecha != null && ChronoUnit.DAYS.between(ultimaFecha, hoy) >= diasInactivo;
    }

    private boolean verificarBalanceMayorMesAnterior(List<Transaccion> transacciones, List<Ingreso> ingresos, LocalDate hoy) {
        LocalDate mesActualInicio = hoy.withDayOfMonth(1);
        LocalDate mesAnteriorInicio = mesActualInicio.minusMonths(1);
        LocalDate mesAnteriorFin = mesActualInicio.minusDays(1);

        BigDecimal balanceMesActual = calcularBalancePeriodo(transacciones, ingresos, mesActualInicio, hoy);
        BigDecimal balanceMesAnterior = calcularBalancePeriodo(transacciones, ingresos, mesAnteriorInicio, mesAnteriorFin);

        return balanceMesActual.compareTo(balanceMesAnterior) > 0;
    }

    private boolean verificarIngresosSemanalesSeguidos(List<Ingreso> ingresos, LocalDate hoy, int semanas) {
        for (int i = 0; i < semanas; i++) {
            LocalDate finSemana = hoy.minusWeeks(i);
            LocalDate inicioSemana = finSemana.minusDays(6);

            boolean tieneIngreso = ingresos.stream()
                .filter(Objects::nonNull)
                .map(t -> t.getFecha())
                .filter(Objects::nonNull)
                .anyMatch(fecha -> !fecha.isBefore(inicioSemana) && !fecha.isAfter(finSemana));

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

    private boolean verificarMejoraPorcentajeBalance(List<Transaccion> transacciones, List<Ingreso> ingresos, LocalDate hoy, BigDecimal porcentaje) {
        LocalDate inicioMes = hoy.withDayOfMonth(1);
        BigDecimal balanceInicioMes = calcularBalancePeriodo(transacciones, ingresos, inicioMes, inicioMes);
        BigDecimal balanceHoy = calcularBalancePeriodo(transacciones, ingresos, inicioMes, hoy);

        if (balanceInicioMes.compareTo(BigDecimal.ZERO) <= 0) return false;

        BigDecimal incrementoRequerido = balanceInicioMes.multiply(BigDecimal.ONE.add(porcentaje));
        return balanceHoy.compareTo(incrementoRequerido) >= 0;
    }

    private boolean verificarNumerosPositivosPrimerosDias(List<Transaccion> transacciones, List<Ingreso> ingresos, LocalDate hoy, int diasLimite) {
        if (hoy.getDayOfMonth() < diasLimite) return false;

        LocalDate inicioMes = hoy.withDayOfMonth(1);
        BigDecimal balanceAcumulado = BigDecimal.ZERO;

        for (int i = 1; i <= diasLimite; i++) {
            LocalDate dia = inicioMes.withDayOfMonth(i);
            BigDecimal balanceDia = calcularBalancePeriodo(transacciones, ingresos, dia, dia);
            balanceAcumulado = balanceAcumulado.add(balanceDia);

            if (balanceAcumulado.compareTo(BigDecimal.ZERO) < 0) {
                return false;
            }
        }
        return true;
    }

    private BigDecimal calcularBalancePeriodo(List<Transaccion> transacciones, List<Ingreso> ingresos, LocalDate inicio, LocalDate fin) {
        BigDecimal totalIngresos = ingresos.stream()
                .filter(Objects::nonNull)
                .filter(i -> i.getFecha() != null
                        && !i.getFecha().isBefore(inicio)
                        && !i.getFecha().isAfter(fin))
                .map(t -> t.getMonto())
                .filter(Objects::nonNull)
                .map(t -> t.abs())
                .reduce(BigDecimal.ZERO, (subtotal, amount) -> subtotal.add(amount));

        BigDecimal totalGastos = calcularGastosPeriodo(transacciones, inicio, fin);

        return totalIngresos.subtract(totalGastos);
    }

    private BigDecimal calcularGastosPeriodo(List<Transaccion> transacciones, LocalDate inicio, LocalDate fin) {
        return transacciones.stream()
                .filter(Objects::nonNull)
                .filter(t -> t.getFecha() != null
                        && !t.getFecha().isBefore(inicio)
                        && !t.getFecha().isAfter(fin))
                .map(t -> t.getMonto())
                .filter(Objects::nonNull)
                .map(monto -> monto.abs())
                .reduce(BigDecimal.ZERO, (subtotal, amount) -> subtotal.add(amount));
    }
}