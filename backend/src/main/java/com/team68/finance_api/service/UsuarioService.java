package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.AuthRequestDTO;
import com.team68.finance_api.dto.response.AuthResponseDTO;
import com.team68.finance_api.dto.response.MedallaResponseDTO;
import com.team68.finance_api.model.Medalla;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.MedallaRepository;
import com.team68.finance_api.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final MedallaRepository medallaRepository;

    public UsuarioService(UsuarioRepository usuarioRepository, MedallaRepository medallaRepository) {
        this.usuarioRepository = usuarioRepository;
        this.medallaRepository = medallaRepository;
    }

    public AuthResponseDTO login(AuthRequestDTO request) {
        // En producción/hackathon validas contraseña encriptada
        Usuario usuario = usuarioRepository.findByUsername(request.getUsername())
                .orElseGet(() -> usuarioRepository.save(Usuario.builder()
                        .username(request.getUsername())
                        .password(request.getPassword())
                        .nombre(request.getUsername())
                        .build()));

        return AuthResponseDTO.builder()
                .id(usuario.getId())
                .username(usuario.getUsername())
                .nombre(usuario.getNombre())
                .token("mock-jwt-token-" + usuario.getId())
                .build();
    }

    public List<MedallaResponseDTO> obtenerMedallasUsuario(UUID usuarioId) {
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado"));

        List<Medalla> todasLasMedallas = medallaRepository.findAll();
        Set<UUID> medallasObtenidasIds = usuario.getMedallas().stream()
                .map(m -> m.getId().toString())
                .map(UUID::fromString)
                .collect(Collectors.toSet());

        return todasLasMedallas.stream().map(m -> MedallaResponseDTO.builder()
                .id(m.getId())
                .codigo(m.getCodigo())
                .nombre(m.getNombre())
                .descripcion(m.getDescripcion())
                .iconoUrl(m.getIconoUrl())
                .puntos(m.getPuntos())
                .obtenida(usuario.getMedallas().contains(m))
                .build()
        ).collect(Collectors.toList());
    }
}