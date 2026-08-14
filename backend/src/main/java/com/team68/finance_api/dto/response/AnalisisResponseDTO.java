package com.team68.finance_api.dto.response;

import com.team68.finance_api.dto.request.UsuarioRequestDTO;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.*;

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

    @JsonProperty("recomendacion_general")
    private String recomendacionGeneral;

    @Getter
    @Setter
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class DimensionesWrapperDTO {
        @JsonProperty("balance_financiero")
        private DimensionDetalleDTO balanceFinanciero;

        @JsonProperty("capacidad_de_ahorro")
        private DimensionDetalleDTO capacidadAhorro;

        private DimensionDetalleDTO endeudamiento;

        @JsonProperty("comportamiento_de_consumo")
        private DimensionDetalleDTO comportamientoConsumo;
    }
}