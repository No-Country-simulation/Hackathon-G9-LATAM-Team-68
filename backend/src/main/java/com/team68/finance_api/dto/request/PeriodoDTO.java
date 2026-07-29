package com.team68.finance_api.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.time.LocalDate;


@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PeriodoDTO {

    @NotNull(message = "La fecha de inicio es obligatoria")
    private LocalDate inicio;

    @NotNull(message = "La fecha de fin es obligatoria")
    private LocalDate fin;

}
