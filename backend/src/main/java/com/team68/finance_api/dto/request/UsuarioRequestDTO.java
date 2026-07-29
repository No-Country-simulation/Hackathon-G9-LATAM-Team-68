package com.team68.finance_api.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UsuarioRequestDTO {
    private Long id;

    @NotBlank(message = "El nombre es obligatorio")
    private String nombre;
}