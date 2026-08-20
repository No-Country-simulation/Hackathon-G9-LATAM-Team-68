package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.AnalisisRequestDTO;
import com.team68.finance_api.dto.request.IngresoRequestDTO;
import com.team68.finance_api.dto.request.SolicitudAnalisisDTO;
import com.team68.finance_api.dto.request.TransaccionRequestDTO;
import com.team68.finance_api.dto.request.UsuarioRequestDTO;
import com.team68.finance_api.dto.response.AnalisisResponseDTO;
import com.team68.finance_api.model.Ingreso;
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
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class CalculoFinancieroService {
    @Value("${analisis.api.url}")
    private String analisisApiUrl;

    private final UsuarioRepository usuarioRepository;
    private final IngresoRepository ingresoRepository;
    private final TransaccionRepository transaccionRepository;
    private final RestTemplate restTemplate = new RestTemplate();

    public CalculoFinancieroService(UsuarioRepository usuarioRepository,
                                    IngresoRepository ingresoRepository,
                                    TransaccionRepository transaccionRepository) {
        this.usuarioRepository = usuarioRepository;
        this.ingresoRepository = ingresoRepository;
        this.transaccionRepository = transaccionRepository;
    }

    public AnalisisResponseDTO calcularAnalisisFinanciero(SolicitudAnalisisDTO solicitud) {
        UUID usuarioId = java.util.Objects.requireNonNull(
                solicitud.getUsuarioId(),
                "El ID del usuario no puede ser nulo"
        );

        // 1. Buscar Usuario en la base de datos
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado con ID: " + usuarioId));

        if (solicitud.getPeriodo() == null ||
            solicitud.getPeriodo().getInicio() == null ||
            solicitud.getPeriodo().getFin() == null) {
            throw new IllegalArgumentException("El periodo con fecha de inicio y fin es obligatorio");
        }

        LocalDate fechaInicio = LocalDate.parse(solicitud.getPeriodo().getInicio());
        LocalDate fechaFin = LocalDate.parse(solicitud.getPeriodo().getFin());

        // 2. Buscar Ingresos y Transacciones en el rango de fechas
        List<Ingreso> ingresosEntities = ingresoRepository.findByUsuarioIdAndFechaBetween(usuarioId, fechaInicio, fechaFin);
        List<Transaccion> transaccionesEntities = transaccionRepository.findByUsuarioIdAndFechaBetween(usuarioId, fechaInicio, fechaFin);

        // 3. Mapear Usuario (id pasa directamente como UUID)
        UsuarioRequestDTO usuarioDTO = UsuarioRequestDTO.builder()
                .id(usuario.getId())
                .nombre(usuario.getNombre())
                .build();

        // 4. Mapear Ingresos
        List<IngresoRequestDTO> ingresosDTO = ingresosEntities.stream()
            .map(i -> IngresoRequestDTO.builder()
                    .fecha(i.getFecha()) // Pasa directamente el LocalDate/Date
                    .descripcion(i.getDescripcion())
                    .monto(i.getMonto())
                    .build())
            .collect(Collectors.toList());

        // 5. Mapear Transacciones
        List<TransaccionRequestDTO> transaccionesDTO = transaccionesEntities.stream()
            .map(t -> {
                // Verificar si es tarjeta de crédito (ignorando mayúsculas/minúsculas o acentos si aplica)
                boolean esTarjetaCredito = t.getFormaPago() != null &&
                        t.getFormaPago().equalsIgnoreCase("Tarjeta de crédito");

                return TransaccionRequestDTO.builder()
                        .fecha(t.getFecha())
                        .descripcion(t.getDescripcion())
                        .monto(t.getMonto())
                        .formaPago(t.getFormaPago())
                        // Si no es tarjeta de crédito, se envía null
                        .tasaDeInteresDeLaTarjeta(esTarjetaCredito ? t.getTasaDeInteresDeLaTarjeta() : null)
                        .build();
            })
            .collect(Collectors.toList());

        // 6. Armar el payload completo para el servicio externo
        AnalisisRequestDTO payload = AnalisisRequestDTO.builder()
                .usuario(usuarioDTO)
                .periodo(solicitud.getPeriodo())
                .ingresos(ingresosDTO)
                .transacciones(transaccionesDTO)
                .build();

        // 7. Peticion HTTP POST
        String url = analisisApiUrl.replaceAll("/+$", "") + "/analizar";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<AnalisisRequestDTO> entity = new HttpEntity<>(payload, headers);

        ResponseEntity<AnalisisResponseDTO> response = restTemplate.postForEntity(
                url,
                entity,
                AnalisisResponseDTO.class
        );

        return response.getBody();
    }
}