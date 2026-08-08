package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.TransaccionRequestDTO;
import com.team68.finance_api.model.CategoriaConsumo;
import com.team68.finance_api.model.TipoFinanciero;
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
        // Validacion Cruzada de Negocio
        validarReglaTipoYCategoria(dto.getTipoFinanciero(), dto.getCategoria());

        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado con ID: " + usuarioId));

        Transaccion t = Transaccion.builder()
                .usuario(usuario)
                .fecha(dto.getFecha())
                .descripcion(dto.getDescripcion())
                .monto(dto.getMonto())
                .formaPago(dto.getFormaPago())
                .tasaDeInteresDeLaTarjeta(dto.getTasaDeInteresDeLaTarjeta())
                .tipoFinanciero(dto.getTipoFinanciero())
                .categoria(dto.getCategoria())
                .build();

        return transaccionRepository.save(t);
    }

    public void validarReglaTipoYCategoria(TipoFinanciero tipo, CategoriaConsumo categoria) {
        if (tipo == TipoFinanciero.PAGO_DEUDA || tipo == TipoFinanciero.AHORRO_INVERSION) {
            if (categoria != null) {
                throw new IllegalArgumentException("Para movimientos de tipo PAGO_DEUDA o AHORRO_INVERSION, el campo categoría debe ser nulo.");
            }
        } else if (tipo == TipoFinanciero.CONSUMO) {
            if (categoria == null) {
                throw new IllegalArgumentException("Para movimientos de tipo CONSUMO, la categoría es estrictamente obligatoria.");
            }
        }
    }
}