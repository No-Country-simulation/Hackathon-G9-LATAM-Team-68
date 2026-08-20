package com.team68.finance_api.dto.response;

import lombok.*;

import java.util.Map;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PerfilFinancieroDTO {

    private Integer puntuacion;
    private String estado;
    private Map<String, Integer> dimensiones;
}
