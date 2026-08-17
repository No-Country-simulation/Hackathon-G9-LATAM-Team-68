package com.team68.finance_api.model;

import com.fasterxml.jackson.annotation.JsonCreator;

public enum TipoFinanciero {
    CONSUMO,
    PAGO_DEUDA,
    AHORRO_INVERSION,
    OTROS;

    @JsonCreator
    public static TipoFinanciero fromString(String value) {
        if (value == null) return OTROS;
        for (TipoFinanciero type : TipoFinanciero.values()) {
            if (type.name().equalsIgnoreCase(value.trim()) || 
                type.name().replace("_", "").equalsIgnoreCase(value.replace(" ", "").trim())) {
                return type;
            }
        }
        return OTROS;
    }
}