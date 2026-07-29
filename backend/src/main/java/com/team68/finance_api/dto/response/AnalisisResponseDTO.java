package com.team68.finance_api.dto.response;

import com.team68.finance_api.dto.request.UsuarioRequestDTO;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.*;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AnalisisResponseDTO {

    private UsuarioRequestDTO usuario;

    @JsonProperty("perfil_financiero")
    private PerfilFinancieroDTO perfilFinanciero;

    private DimensionesWrapperDTO dimensiones;

    @JsonProperty("recomendaciones_generales")
    private List<String> recomendacionesGenerales;

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class DimensionesWrapperDTO {
        @JsonProperty("balance_financiero")
        private DimensionDetalleDTO balanceFinanciero;

        @JsonProperty("capacidad_ahorro")
        private DimensionDetalleDTO capacidadAhorro;

        private DimensionDetalleDTO endeudamiento;

        @JsonProperty("comportamiento_consumo")
        private DimensionDetalleDTO comportamientoConsumo;
    }
}