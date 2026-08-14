package com.team68.finance_api.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PeriodoDTO {
    @NotBlank(message = "La fecha de inicio es obligatoria")
    @JsonProperty("inicio")
    private String inicio;

    @NotBlank(message = "La fecha de fin es obligatoria")
    @JsonProperty("fin")
    private String fin;
}