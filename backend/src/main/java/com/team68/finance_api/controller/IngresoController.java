package com.team68.finance_api.controller;

import com.team68.finance_api.dto.request.IngresoRequestDTO;
import com.team68.finance_api.model.Ingreso;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.IngresoRepository;
import com.team68.finance_api.repository.UsuarioRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/ingresos")
@CrossOrigin(origins = "*")
public class IngresoController {

    private final IngresoRepository ingresoRepository;
    private final UsuarioRepository usuarioRepository;

    public IngresoController(IngresoRepository ingresoRepository, UsuarioRepository usuarioRepository) {
        this.ingresoRepository = ingresoRepository;
        this.usuarioRepository = usuarioRepository;
    }


    @PostMapping("/usuario/{usuarioId}")
    public ResponseEntity<Ingreso> crearIngreso(@PathVariable UUID usuarioId,
                                                @Valid @RequestBody IngresoRequestDTO dto){

        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado"));

        Ingreso ingreso = new Ingreso();
        ingreso.setUsuario(usuario);
        ingreso.setFecha(dto.getFecha());
        ingreso.setDescripcion(dto.getDescripcion());
        ingreso.setMonto(dto.getMonto());
        ingreso.setEsIngreso(true);

        Ingreso savedIngreso = ingresoRepository.save(ingreso);

        return ResponseEntity.status(HttpStatus.CREATED).body(savedIngreso);

    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<Ingreso>> obtenerIngresosUsuario(@PathVariable UUID usuarioId){

      return ResponseEntity.ok(ingresoRepository.findByUsuarioId(usuarioId));


    }

}
