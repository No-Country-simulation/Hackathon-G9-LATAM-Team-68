package com.team68.finance_api.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IngresoRequestDTO {
    @NotNull(message = "La fecha del ingreso es obligatoria")
    private LocalDate fecha;

    @NotBlank(message = "La descripción del ingreso no puede estar vacía")
    private String descripcion;

    @NotNull(message = "El monto del ingreso es obligatorio")
    @Positive(message = "El monto del ingreso debe ser un valor mayor a cero")
    private BigDecimal monto;
}