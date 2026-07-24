package com.team68.finance_api.model;

public enum CategoriaConsumo {
    VIVIENDA(GrupoCategoria.ESENCIAL, "Vivienda"),
    ALIMENTACION(GrupoCategoria.ESENCIAL, "Alimentación"),
    TRANSPORTE(GrupoCategoria.ESENCIAL, "Transporte"),
    SALUD(GrupoCategoria.ESENCIAL, "Salud"),
    EDUCACION(GrupoCategoria.ESENCIAL, "Educación"),
    ENTRETENIMIENTO_Y_OCIO(GrupoCategoria.DISCRECIONAL, "Entretenimiento y ocio"),
    SUSCRIPCIONES_DIGITALES(GrupoCategoria.DISCRECIONAL, "Suscripciones digitales"),
    COMPRAS_PERSONALES(GrupoCategoria.DISCRECIONAL, "Compras personales"),
    VIAJES_Y_VACACIONES(GrupoCategoria.DISCRECIONAL, "Viajes y vacaciones"),
    OTROS(GrupoCategoria.DISCRECIONAL, "Otros");

    private final GrupoCategoria grupo;
    private final String nombreFormateado;

    CategoriaConsumo(GrupoCategoria grupo, String nombreFormateado) {
        this.grupo = grupo;
        this.nombreFormateado = nombreFormateado;
    }

    public GrupoCategoria getGrupo() {
        return grupo;
    }

    public String getNombreFormateado() {
    return nombreFormateado;
    }
}