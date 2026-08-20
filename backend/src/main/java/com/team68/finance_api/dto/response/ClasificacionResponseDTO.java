package com.team68.finance_api.dto.response;

import com.team68.finance_api.model.CategoriaConsumo;
import com.team68.finance_api.model.TipoFinanciero;
import com.fasterxml.jackson.annotation.JsonAlias;
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
        @JsonAlias({"clasificacion", "tipoFinanciero", "tipo"})
        private Object tipoFinancieroRaw;

        @JsonProperty("categoria")
        @JsonAlias({"categoria_consumo", "categoriaConsumo"})
        private CategoriaConsumo categoria;

        public TipoFinanciero getTipoFinanciero() {
            if (tipoFinancieroRaw == null) {
                return TipoFinanciero.CONSUMO;
            }

            // Si la IA regresa un array: ["Pago de deuda"]
            if (tipoFinancieroRaw instanceof List<?> list && !list.isEmpty()) {
                return TipoFinanciero.fromString(list.get(0).toString());
            }

            return TipoFinanciero.fromString(tipoFinancieroRaw.toString());
        }
    }
}