package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.AuthRequestDTO;
import com.team68.finance_api.dto.response.AuthResponseDTO;
import com.team68.finance_api.dto.response.MedallaResponseDTO;
import com.team68.finance_api.model.Medalla;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.MedallaRepository;
import com.team68.finance_api.repository.UsuarioRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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

    @SuppressWarnings("null")
    @Transactional
    public AuthResponseDTO login(AuthRequestDTO request) {
        // Buscar usuario con sus medallas inicializadas o crearlo
        Optional<Usuario> usuarioOpt = usuarioRepository.findByUsernameWithMedallas(request.getUsername());
        Usuario usuario;

        if (usuarioOpt.isPresent()) {
            usuario = usuarioOpt.get();
        } else {
            usuario = Usuario.builder()
                    .username(request.getUsername())
                    .password(request.getPassword())
                    .nombre(request.getUsername())
                    .medallas(new HashSet<>())
                    .build();
        }

        // Asignar medalla de bienvenida si no la tiene
        medallaRepository.findByCodigo("PEQUENO_OSEZNO").ifPresent(medalla -> {
            if (!usuario.getMedallas().contains(medalla)) {
                usuario.getMedallas().add(medalla);
            }
        });

        usuarioRepository.save(usuario);

        return AuthResponseDTO.builder()
                .id(usuario.getId())
                .username(usuario.getUsername())
                .nombre(usuario.getNombre())
                .token("mock-jwt-token-" + usuario.getId())
                .build();
    }

    @Transactional(readOnly = true)
    public List<MedallaResponseDTO> obtenerMedallasUsuario(UUID usuarioId) {
        Usuario usuario = usuarioRepository.findByIdWithMedallas(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado"));

        List<Medalla> todasLasMedallas = medallaRepository.findAll();

        Set<Long> medallasObtenidasIds = usuario.getMedallas().stream()
                .filter(Objects::nonNull)
                .map(m -> m.getId())
                .filter(Objects::nonNull)
                .collect(Collectors.toSet());

        return todasLasMedallas.stream()
                .filter(Objects::nonNull)
                .map(m -> MedallaResponseDTO.builder()
                        .id(m.getId())
                        .codigo(m.getCodigo())
                        .nombre(m.getNombre())
                        .descripcion(m.getDescripcion())
                        .iconoUrl(m.getIconoUrl())
                        .puntos(m.getPuntos())
                        .obtenida(medallasObtenidasIds.contains(m.getId()))
                        .build()
                )
                .collect(Collectors.toList());
    }
}