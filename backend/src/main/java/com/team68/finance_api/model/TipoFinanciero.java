package com.team68.finance_api.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import java.text.Normalizer;

public enum TipoFinanciero {
    CONSUMO,
    PAGO_DEUDA,
    AHORRO_INVERSION;

    @JsonCreator
    public static TipoFinanciero fromString(Object input) {
        if (input == null) return CONSUMO;

        String value = input.toString();
        if (value.isBlank()) return CONSUMO;

        // Normalizar quita acentos (ej: "Inversión" -> "Inversion")
        String normalized = Normalizer.normalize(value, Normalizer.Form.NFD)
                .replaceAll("\\p{M}", "");

        String cleanValue = normalized.trim().toUpperCase()
                .replace("PAGO DE DEUDA", "PAGO_DEUDA")
                .replace("AHORRO E INVERSION", "AHORRO_INVERSION")
                .replace("AHORRO Y INVERSION", "AHORRO_INVERSION")
                .replace("/", "_")
                .replace("-", "_")
                .replace(" ", "_");

        for (TipoFinanciero type : TipoFinanciero.values()) {
            if (type.name().equalsIgnoreCase(cleanValue) ||
                cleanValue.contains(type.name())) {
                return type;
            }
        }

        // Fallback seguro para la restriccion CHECK de la BD
        return CONSUMO;
    }
}