package com.team68.finance_api.controller;

import com.team68.finance_api.dto.request.TransaccionRequestDTO;
import com.team68.finance_api.model.Transaccion;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.TransaccionRepository;
import com.team68.finance_api.repository.UsuarioRepository;
import com.team68.finance_api.service.ClasificacionService;
import com.team68.finance_api.service.GamificacionService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/movimientos")
@CrossOrigin(origins = "*")
public class MovimientoController {

    private final TransaccionRepository transaccionRepository;
    private final UsuarioRepository usuarioRepository;
    private final GamificacionService gamificacionService;
    private final ClasificacionService clasificacionService;

    public MovimientoController(TransaccionRepository transaccionRepository,
                                UsuarioRepository usuarioRepository,
                                GamificacionService gamificacionService,
                                ClasificacionService clasificacionService) {
        this.transaccionRepository = transaccionRepository;
        this.usuarioRepository = usuarioRepository;
        this.gamificacionService = gamificacionService;
        this.clasificacionService = clasificacionService;
    }

    @PostMapping("/usuario/{usuarioId}")
    public ResponseEntity<Transaccion> crearTransaccion(@PathVariable @NonNull UUID usuarioId,
                                                        @Valid @RequestBody TransaccionRequestDTO dto) {
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado"));

        Transaccion transaccion = Transaccion.builder()
                .usuario(usuario)
                .fecha(dto.getFecha())
                .descripcion(dto.getDescripcion())
                .monto(dto.getMonto())
                .formaPago(dto.getFormaPago())
                .tasaDeInteresDeLaTarjeta(dto.getTasaDeInteresDeLaTarjeta())
                .build();

        transaccionRepository.save(transaccion);

        // Re-clasificar todas las transacciones del usuario
        clasificacionService.clasificarYGuardarTodasLasTransacciones(usuarioId);

        // Evaluar medallas automáticamente tras registrar el nuevo movimiento
        gamificacionService.evaluarYAsignarMedallas(usuarioId);

        // Obtener la transacción ya clasificada desde la BD
        Transaccion transaccionActualizada = transaccionRepository.findById(transaccion.getId())
                .orElse(transaccion);

        return ResponseEntity.status(HttpStatus.CREATED).body(transaccionActualizada);
    }

    @PostMapping("/clasificar/usuario/{usuarioId}")
    public ResponseEntity<List<Transaccion>> clasificarTransaccionesExistentes(@PathVariable @NonNull UUID usuarioId) {
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado con ID: " + usuarioId));

        List<Transaccion> transaccionesClasificadas = clasificacionService.clasificarYGuardarTodasLasTransacciones(usuario.getId());

        return ResponseEntity.ok(transaccionesClasificadas);
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<Transaccion>> obtenerMovimientosUsuario(@PathVariable UUID usuarioId){
        return ResponseEntity.ok(transaccionRepository.findByUsuarioId(usuarioId));
    }

    @PutMapping("/{transaccionId}")
    public ResponseEntity<Transaccion> actualizarTransaccion(@PathVariable @NonNull UUID transaccionId,
                                                             @Valid @RequestBody TransaccionRequestDTO dto){
        Transaccion transaccion = transaccionRepository.findById(transaccionId)
                .orElseThrow(() -> new IllegalArgumentException("Transaccion no encontrada"));

        transaccion.setFecha(dto.getFecha());
        transaccion.setDescripcion(dto.getDescripcion());
        transaccion.setMonto(dto.getMonto());
        transaccion.setFormaPago(dto.getFormaPago());
        transaccion.setTasaDeInteresDeLaTarjeta(dto.getTasaDeInteresDeLaTarjeta());

        transaccionRepository.save(transaccion);

        // Re-clasificar todas las transacciones del usuario
        clasificacionService.clasificarYGuardarTodasLasTransacciones(transaccion.getUsuario().getId());

        Transaccion transaccionActualizada = transaccionRepository.findById(transaccionId)
                .orElse(transaccion);

        return ResponseEntity.ok(transaccionActualizada);
    }

    @DeleteMapping("/{transaccionId}")
    public ResponseEntity<Void> eliminarTransaccion(@PathVariable @NonNull UUID transaccionId){
        Transaccion transaccion = transaccionRepository.findById(transaccionId)
                .orElseThrow(() -> new IllegalArgumentException("Transaccion no encontrada"));

        transaccionRepository.delete(transaccion);

        return ResponseEntity.noContent().build();
    }
}