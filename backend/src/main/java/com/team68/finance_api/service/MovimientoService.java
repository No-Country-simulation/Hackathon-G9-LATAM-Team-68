package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.TransaccionRequestDTO;
import com.team68.finance_api.model.Transaccion;
import com.team68.finance_api.model.Usuario;
import com.team68.finance_api.repository.TransaccionRepository;
import com.team68.finance_api.repository.UsuarioRepository;

import org.springframework.lang.NonNull;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class MovimientoService {

    private final TransaccionRepository transaccionRepository;
    private final UsuarioRepository usuarioRepository;

    public MovimientoService(TransaccionRepository transaccionRepository, UsuarioRepository usuarioRepository) {
        this.transaccionRepository = transaccionRepository;
        this.usuarioRepository = usuarioRepository;
    }

    @SuppressWarnings("null")
    public Transaccion guardarTransaccion(@NonNull UUID usuarioId, TransaccionRequestDTO dto) {
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado con ID: " + usuarioId));

        Transaccion t = Transaccion.builder()
                .usuario(usuario)
                .fecha(dto.getFecha())
                .descripcion(dto.getDescripcion())
                .monto(dto.getMonto())
                .formaPago(dto.getFormaPago())
                .tasaDeInteresDeLaTarjeta(dto.getTasaDeInteresDeLaTarjeta())
                .build();

        return transaccionRepository.save(t);
    }
}