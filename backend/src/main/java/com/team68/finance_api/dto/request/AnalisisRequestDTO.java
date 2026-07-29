package com.team68.finance_api.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import lombok.*;

import java.math.BigDecimal;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AnalisisRequestDTO {
    @Valid
    @NotNull(message = "La información del usuario es obligatoria")
    private UsuarioRequestDTO usuario;

    @Valid
    @NotNull(message = "El periodo del análisis es obligatorio")
    private PeriodoDTO periodo;

    @JsonProperty("ingreso_mensual")
    @NotNull(message = "El ingreso mensual es obligatorio")
    @Positive(message = "El ingreso mensual debe ser un número positivo")
    private BigDecimal ingresoMensual;

    @Valid
    @NotEmpty(message = "Debe proporcionar al menos una transacción para realizar el análisis")
    private List<TransaccionRequestDTO> transacciones;

}
