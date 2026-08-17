package com.team68.finance_api.dto.response;

import com.team68.finance_api.model.CategoriaConsumo;
import com.team68.finance_api.model.TipoFinanciero;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClasificacionResponseDTO {
    private List<TransaccionClasificadaDTO> transacciones;

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class TransaccionClasificadaDTO {
        private String descripcion;

        @JsonProperty("tipo_financiero")
        private TipoFinanciero tipoFinanciero;

        private CategoriaConsumo categoria;
    }
}