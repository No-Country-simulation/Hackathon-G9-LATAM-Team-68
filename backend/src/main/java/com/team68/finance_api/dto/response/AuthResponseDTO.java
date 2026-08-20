package com.team68.finance_api.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class AuthResponseDTO {
    private UUID id;
    private String username;
    private String nombre;
    private String token; // Para Auth JWT o Token simulado
}