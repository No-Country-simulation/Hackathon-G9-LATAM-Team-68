package com.team68.finance_api.controller;

import com.team68.finance_api.dto.response.MedallaResponseDTO;
import com.team68.finance_api.service.UsuarioService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/medallas")
@CrossOrigin(origins = "*")
public class GamificacionController {

    private final UsuarioService usuarioService;

    public GamificacionController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<MedallaResponseDTO>> obtenerMedallas(@PathVariable UUID usuarioId) {
        return ResponseEntity.ok(usuarioService.obtenerMedallasUsuario(usuarioId));
    }
}