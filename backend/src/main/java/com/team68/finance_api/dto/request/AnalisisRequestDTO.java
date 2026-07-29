package com.team68.finance_api.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AnalisisRequestDTO {

    @Valid
    @NotNull(message = "Los datos del usuario son obligatorios")
    private UsuarioRequestDTO usuario;

    @Valid
    @NotNull(message = "El periodo es obligatorio")
    private PeriodoDTO periodo;

    @Valid
    @NotEmpty(message = "Debe proporcionar al menos un ingreso")
    private List<IngresoRequestDTO> ingresos;

    @Valid
    @NotEmpty(message = "Debe proporcionar al menos una transacción")
    private List<TransaccionRequestDTO> transacciones;
}