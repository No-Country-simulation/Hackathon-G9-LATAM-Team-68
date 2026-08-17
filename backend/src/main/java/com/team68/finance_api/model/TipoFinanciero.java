package com.team68.finance_api.model;

import com.fasterxml.jackson.annotation.JsonCreator;

public enum TipoFinanciero {
    CONSUMO,
    PAGO_DEUDA,
    AHORRO_INVERSION,
    OTROS;

    @JsonCreator
    public static TipoFinanciero fromString(String value) {
        if (value == null || value.isBlank()) return OTROS;

        String cleanValue = value.trim().toUpperCase()
                .replace("/", "_")
                .replace("-", "_")
                .replace(" ", "_");

        for (TipoFinanciero type : TipoFinanciero.values()) {
            if (type.name().equalsIgnoreCase(cleanValue) ||
                type.name().replace("_", "").equalsIgnoreCase(cleanValue.replace("_", ""))) {
                return type;
            }
        }
        return OTROS;
    }
}