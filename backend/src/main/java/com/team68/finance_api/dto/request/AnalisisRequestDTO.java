package com.team68.finance_api.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
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
    @JsonProperty("usuario")
    private UsuarioRequestDTO usuario;

    @Valid
    @NotNull(message = "El periodo es obligatorio")
    @JsonProperty("periodo")
    private PeriodoDTO periodo;

    @Valid
    @NotEmpty(message = "Debe proporcionar al menos un ingreso")
    @JsonProperty("ingresos")
    private List<IngresoRequestDTO> ingresos;

    @Valid
    @NotEmpty(message = "Debe proporcionar al menos una transacción")
    @JsonProperty("transacciones")
    private List<TransaccionRequestDTO> transacciones;
}