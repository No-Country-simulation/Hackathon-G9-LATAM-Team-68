package com.team68.finance_api.dto.response;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class MedallaResponseDTO {
    private Long id;
    private String codigo;
    private String nombre;
    private String descripcion;
    private String iconoUrl;
    private Integer puntos;
    private boolean obtenida;
}