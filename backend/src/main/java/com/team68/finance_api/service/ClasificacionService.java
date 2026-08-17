package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.AnalisisRequestDTO;
import com.team68.finance_api.dto.request.IngresoRequestDTO;
import com.team68.finance_api.dto.request.PeriodoDTO;
import com.team68.finance_api.dto.request.TransaccionRequestDTO;
import com.team68.finance_api.dto.request.UsuarioRequestDTO;
import com.team68.finance_api.dto.response.ClasificacionResponseDTO;
import com.team68.finance_api.model.CategoriaConsumo;
import com.team68.finance_api.model.Ingreso;
import com.team68.finance_api.model.TipoFinanciero;
import com.team68.finance_api.model.Transaccion;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.IngresoRepository;
import com.team68.finance_api.repository.TransaccionRepository;
import com.team68.finance_api.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.util.Comparator;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class ClasificacionService {
    @Value("${analisis.api.url}")
    private String analisisApiUrl;

    private final TransaccionRepository transaccionRepository;
    private final IngresoRepository ingresoRepository;
    private final UsuarioRepository usuarioRepository;
    private final RestTemplate restTemplate = new RestTemplate();

    public ClasificacionService(TransaccionRepository transaccionRepository,
                                IngresoRepository ingresoRepository,
                                UsuarioRepository usuarioRepository) {
        this.transaccionRepository = transaccionRepository;
        this.ingresoRepository = ingresoRepository;
        this.usuarioRepository = usuarioRepository;
    }

    @Transactional
    public List<Transaccion> clasificarYGuardarTodasLasTransacciones(@NonNull UUID usuarioId) {
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado con ID: " + usuarioId));

        List<Transaccion> transacciones = transaccionRepository.findByUsuarioId(usuarioId);

        if (transacciones.isEmpty()) {
            return transacciones;
        }

        List<Ingreso> ingresos = ingresoRepository.findByUsuarioId(usuarioId);

        // 1. Mapear Usuario
        UsuarioRequestDTO usuarioDTO = UsuarioRequestDTO.builder()
                .id(usuario.getId())
                .nombre(usuario.getNombre())
                .build();

        // 2. Mapear Ingresos
        List<IngresoRequestDTO> ingresosDTO = ingresos.stream()
                .map(i -> IngresoRequestDTO.builder()
                        .fecha(i.getFecha())
                        .descripcion(i.getDescripcion())
                        .monto(i.getMonto())
                        .build())
                .collect(Collectors.toList());

        // 3. Mapear Transacciones
        List<TransaccionRequestDTO> transaccionesDTO = transacciones.stream()
                .map(t -> {
                    boolean esTarjetaCredito = t.getFormaPago() != null &&
                            t.getFormaPago().equalsIgnoreCase("Tarjeta de crédito");

                    return TransaccionRequestDTO.builder()
                            .fecha(t.getFecha())
                            .descripcion(t.getDescripcion())
                            .monto(t.getMonto())
                            .formaPago(t.getFormaPago())
                            .tasaDeInteresDeLaTarjeta(esTarjetaCredito ? t.getTasaDeInteresDeLaTarjeta() : null)
                            .build();
                })
                .collect(Collectors.toList());

        // 4. Calcular el Periodo dinámicamente según el rango de fechas existente
        PeriodoDTO periodoDTO = calcularPeriodo(transacciones, ingresos);

        // 5. Construir el payload idéntico a /analizar
        AnalisisRequestDTO payload = AnalisisRequestDTO.builder()
                .usuario(usuarioDTO)
                .periodo(periodoDTO)
                .ingresos(ingresosDTO)
                .transacciones(transaccionesDTO)
                .build();

        // 6. Petición POST a /clasificar
        String url = analisisApiUrl.replaceAll("/+$", "") + "/clasificar";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<AnalisisRequestDTO> entity = new HttpEntity<>(payload, headers);
        ResponseEntity<ClasificacionResponseDTO> response = restTemplate.postForEntity(
                url,
                entity,
                ClasificacionResponseDTO.class
        );

        ClasificacionResponseDTO responseBody = response.getBody();

        // 7. Actualizar las transacciones en DB con los resultados devueltos
        if (responseBody != null && responseBody.getTransacciones() != null) {
            List<ClasificacionResponseDTO.TransaccionClasificadaDTO> clasificadas = responseBody.getTransacciones();

            for (int i = 0; i < transacciones.size() && i < clasificadas.size(); i++) {
                Transaccion t = transacciones.get(i);
                ClasificacionResponseDTO.TransaccionClasificadaDTO c = clasificadas.get(i);

                t.setTipoFinanciero(c.getTipoFinanciero());

                if (c.getTipoFinanciero() != TipoFinanciero.CONSUMO ||
                        c.getTipoFinanciero() == TipoFinanciero.PAGO_DEUDA ||
                        c.getTipoFinanciero() == TipoFinanciero.AHORRO_INVERSION) {
                    t.setCategoria(CategoriaConsumo.OTROS);
                } else {
                    t.setCategoria(c.getCategoria());
                }
            }

            return transaccionRepository.saveAll(transacciones);
        }

        return transacciones;
    }

    private PeriodoDTO calcularPeriodo(List<Transaccion> transacciones, List<Ingreso> ingresos) {
        var fechaMinTransaccion = transacciones.stream().map(t -> t.getFecha()).min(Comparator.naturalOrder());
        var fechaMaxTransaccion = transacciones.stream().map(t -> t.getFecha()).max(Comparator.naturalOrder());

        var fechaMinIngreso = ingresos.stream().map(t -> t.getFecha()).min(Comparator.naturalOrder());
        var fechaMaxIngreso = ingresos.stream().map(t -> t.getFecha()).max(Comparator.naturalOrder());

        var fechaInicio = fechaMinTransaccion.orElseGet(() -> fechaMinIngreso.orElse(null));
        var fechaFin = fechaMaxTransaccion.orElseGet(() -> fechaMaxIngreso.orElse(null));

        if (fechaInicio != null && fechaMinIngreso.isPresent() && fechaMinIngreso.get().isBefore(fechaInicio)) {
            fechaInicio = fechaMinIngreso.get();
        }

        if (fechaFin != null && fechaMaxIngreso.isPresent() && fechaMaxIngreso.get().isAfter(fechaFin)) {
            fechaFin = fechaMaxIngreso.get();
        }

        PeriodoDTO periodo = new PeriodoDTO();
        periodo.setInicio(fechaInicio != null ? fechaInicio.toString() : null);
        periodo.setFin(fechaFin != null ? fechaFin.toString() : null);
        return periodo;
    }
}