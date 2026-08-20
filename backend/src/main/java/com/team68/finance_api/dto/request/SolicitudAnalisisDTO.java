package com.team68.finance_api.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SolicitudAnalisisDTO {
    @NotNull(message = "El ID del usuario es obligatorio")
    @JsonProperty("usuario_id")
    private UUID usuarioId;

    @Valid
    @NotNull(message = "El periodo es obligatorio")
    @JsonProperty("periodo")
    private PeriodoDTO periodo;
}