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
    @JsonProperty("puntuacion")
    private Integer puntuacion;

    @JsonProperty("estado")
    private String estado;

    @JsonProperty("indicadores")
    private Map<String, Object> indicadores;

    @JsonProperty("recomendaciones")
    private List<String> recomendaciones;
}