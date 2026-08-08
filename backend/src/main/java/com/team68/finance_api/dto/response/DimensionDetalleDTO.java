package com.team68.finance_api.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;
import java.util.List;
import java.util.Map;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class DimensionDetalleDTO {
    private Integer puntuacion;
    private String estado;
    private Map<String, Object> indicadores;

    private List<String> recomendaciones;
}
