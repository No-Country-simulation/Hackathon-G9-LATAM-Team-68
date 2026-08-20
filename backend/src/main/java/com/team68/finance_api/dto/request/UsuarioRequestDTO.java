package com.team68.finance_api.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.*;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UsuarioRequestDTO {
    private UUID id;

    @NotBlank(message = "El usuario es obligatorio")
    private String nombre;
}