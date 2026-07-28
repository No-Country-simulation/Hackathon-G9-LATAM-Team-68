package com.team68.finance_api.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UsuarioRequestDTO {
    private Long id;

    @NotBlank(message = "El nombre de usuario es obligatorio")
    private String nombre;

    @Email(message = "Debe proporcionar un correo electrónico válido")
    private String email;

    @NotNull(message = "El ingreso mensual es obligatorio")
    @Positive(message = "El ingreso mensual debe ser un valor positivo")
    private BigDecimal ingresoMensual;

    private String frecuenciaAhorro;
}
