package com.team68.finance_api.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import lombok.Getter;

@Getter
public enum CategoriaConsumo {
    VIVIENDA("Vivienda", GrupoCategoria.ESENCIAL),
    ALIMENTACION("Alimentación", GrupoCategoria.ESENCIAL),
    TRANSPORTE("Transporte", GrupoCategoria.ESENCIAL),
    SALUD("Salud", GrupoCategoria.ESENCIAL),
    EDUCACION("Educación", GrupoCategoria.ESENCIAL),
    ENTRETENIMIENTO("Entretenimiento y ocio", GrupoCategoria.DISCRECIONAL),
    SUSCRIPCIONES("Suscripciones digitales", GrupoCategoria.DISCRECIONAL),
    COMPRAS_PERSONALES("Compras personales", GrupoCategoria.DISCRECIONAL),
    VIAJES("Viajes y vacaciones", GrupoCategoria.DISCRECIONAL),
    OTROS("Otros", GrupoCategoria.DISCRECIONAL);

    private final String nombreFormateado;
    private final GrupoCategoria grupo;

    CategoriaConsumo(String nombreFormateado, GrupoCategoria grupo) {
        this.nombreFormateado = nombreFormateado;
        this.grupo = grupo;
    }

    @JsonCreator
    public static CategoriaConsumo fromString(String value) {
        if (value == null || value.isBlank()) return OTROS;

        String cleanValue = value.trim().toUpperCase()
                .replace("Á", "A").replace("É", "E").replace("Í", "I")
                .replace("Ó", "O").replace("Ú", "U")
                .replace(" ", "_");

        for (CategoriaConsumo cat : CategoriaConsumo.values()) {
            if (cat.name().equalsIgnoreCase(cleanValue) ||
                cat.nombreFormateado.equalsIgnoreCase(value.trim())) {
                return cat;
            }
        }
        return OTROS;
    }
}