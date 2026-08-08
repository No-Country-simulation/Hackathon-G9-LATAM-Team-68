package com.team68.finance_api.controller;

import com.team68.finance_api.dto.request.TransaccionRequestDTO;
import com.team68.finance_api.model.Transaccion;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.TransaccionRepository;
import com.team68.finance_api.repository.UsuarioRepository;
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

    public MovimientoController(TransaccionRepository transaccionRepository, UsuarioRepository usuarioRepository) {
        this.transaccionRepository = transaccionRepository;
        this.usuarioRepository = usuarioRepository;
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
                .tipoFinanciero(dto.getTipoFinanciero())
                .categoria(dto.getCategoria())
                .build();

        @SuppressWarnings("null")
        Transaccion savedTransaccion = transaccionRepository.save(transaccion);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedTransaccion);
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<Transaccion>> obtenerMovimientosUsuario(@PathVariable UUID usuarioId){
        return ResponseEntity.ok(transaccionRepository.findByUsuarioId(usuarioId));
    }

}
