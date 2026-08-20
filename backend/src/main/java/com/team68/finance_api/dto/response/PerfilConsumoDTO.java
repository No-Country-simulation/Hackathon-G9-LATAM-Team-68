package com.team68.finance_api.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PerfilConsumoDTO {
    @JsonProperty("predominio_del_gasto")
    private String predominioGasto;

    @JsonProperty("tipo_de_consumo")
    private String tipoConsumo;

    @JsonProperty("diversificacion_del_consumo")
    private String diversificacionConsumo;

    @JsonProperty("categoria_predominante")
    private String categoriaPredominante;
}