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
    @JsonProperty("usuario")
    private UsuarioRequestDTO usuario;

    @JsonProperty("periodo")
    private PeriodoDTO periodo;

    @JsonProperty("ingresos")
    private List<IngresoRequestDTO> ingresos;

    @JsonProperty("transacciones")
    private List<TransaccionRequestDTO> transacciones;
}