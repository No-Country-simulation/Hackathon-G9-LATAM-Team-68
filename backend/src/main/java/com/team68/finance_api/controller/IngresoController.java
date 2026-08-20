package com.team68.finance_api.controller;

import com.team68.finance_api.dto.request.IngresoRequestDTO;
import com.team68.finance_api.model.Ingreso;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.IngresoRepository;
import com.team68.finance_api.repository.UsuarioRepository;
import com.team68.finance_api.service.GamificacionService;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/ingresos")
@CrossOrigin(origins = "*")

public class IngresoController {

    private final IngresoRepository ingresoRepository;
    private final UsuarioRepository usuarioRepository;
    private final GamificacionService gamificacionService;

    public IngresoController(IngresoRepository ingresoRepository, UsuarioRepository usuarioRepository, GamificacionService gamificacionService) {
        this.ingresoRepository = ingresoRepository;
        this.usuarioRepository = usuarioRepository;
        this.gamificacionService = gamificacionService;
    }


    @PostMapping("/usuario/{usuarioId}")
    public ResponseEntity<Ingreso> crearIngreso(@PathVariable @NonNull UUID usuarioId,
                                                @Valid @RequestBody IngresoRequestDTO dto){

        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado"));

        Ingreso ingreso = new Ingreso();
        ingreso.setUsuario(usuario);
        ingreso.setFecha(dto.getFecha());
        ingreso.setDescripcion(dto.getDescripcion());
        ingreso.setMonto(dto.getMonto());

        Ingreso savedIngreso = ingresoRepository.save(ingreso);

        // Evaluar medallas automáticamente tras registrar el nuevo movimiento
        gamificacionService.evaluarYAsignarMedallas(usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED).body(savedIngreso);
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<Ingreso>> obtenerIngresosUsuario(@PathVariable UUID usuarioId){
        return ResponseEntity.ok(ingresoRepository.findByUsuarioId(usuarioId));
    }

    @PutMapping("/{ingresoId}")
    public ResponseEntity<Ingreso> actualizarIngreso(@PathVariable UUID ingresoId,
                                                     @Valid @RequestBody IngresoRequestDTO dto){
        Ingreso ingreso= ingresoRepository.findById(ingresoId)
                .orElseThrow(() -> new IllegalArgumentException("Ingreso no encontrado"));
        ingreso.setFecha(dto.getFecha());
        ingreso.setDescripcion(dto.getDescripcion());
        ingreso.setMonto(dto.getMonto());

        Ingreso ingresoActualizado = ingresoRepository.save(ingreso);

        return ResponseEntity.ok(ingresoActualizado );
    }

    @DeleteMapping("/{ingresoId}")
    public ResponseEntity<Void> eliminarIngreso(@PathVariable UUID ingresoId){

        Ingreso ingreso = ingresoRepository.findById(ingresoId)
                .orElseThrow(() -> new IllegalArgumentException("Ingreso no encontrado"));

        ingresoRepository.delete(ingreso);

        return ResponseEntity.noContent().build();
    }

}
