package com.team68.finance_api.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
public class AnalisisFinancieroController {

    @PostMapping("/analisis-financiero")
    public  Map<String, Object> analizar(@RequestBody Map<String,Object> entrada){
        Map<String, Object> respuesta = new java.util.LinkedHashMap<>();

        Map<String, Object> usuario = Map.of(
                "id", 1,
                "nombre", "Usuario de Prueba"
        );
        respuesta.put("usuario", usuario);

        Map<String, Object> perfilFinanciero = new java.util.LinkedHashMap<>();
        perfilFinanciero.put("puntuacion", 76);
        perfilFinanciero.put("estado", "En observación");
        perfilFinanciero.put("dimensiones", Map.of(
                "balance_financiero", 87,
                "capacidad_ahorro", 64,
                "endeudamiento", 91,
                "comportamiento_consumo", 58
        ));
        respuesta.put("perfil_financiero", perfilFinanciero);


        Map<String, Object> balance = new java.util.LinkedHashMap<>();
        balance.put("estado", "Saludable");
        balance.put("puntuacion", 87);
        balance.put("indicadores", Map.of(
                "balance_mensual", 5500,
                "tasa_gasto", 0.78,
                "margen_financiero", 0.22
        ));
        balance.put("recomendaciones", List.of(
                "Mantener el equilibrio actual entre ingresos y gastos.",
                "Continuar monitoreando el margen financiero mensualmente."
        ));

        Map<String, Object> ahorro = new java.util.LinkedHashMap<>();
        ahorro.put("estado", "En observación");
        ahorro.put("puntuacion", 64);
        ahorro.put("indicadores", Map.of(
                "tasa_ahorro", 0.08,
                "ahorro_inversion_periodo", 2000,
                "aprovechamiento_margen", 0.36
        ));
        ahorro.put("recomendaciones", List.of(
                "Incrementar gradualmente el porcentaje destinado al ahorro.",
                "Aprovechar una mayor parte del margen financiero para ahorro e inversión."
        ));

        Map<String, Object> endeudamiento = new java.util.LinkedHashMap<>();
        endeudamiento.put("estado", "Saludable");
        endeudamiento.put("puntuacion", 91);
        endeudamiento.put("indicadores", Map.of(
                "ratio_endeudamiento", 0.12,
                "pago_deudas", 3000,
                "presion_deuda", "Baja"
        ));
        endeudamiento.put("recomendaciones", List.of(
                "Mantener el nivel actual de endeudamiento.",
                "Evitar adquirir nuevas deudas innecesarias."
        ));

        Map<String, Object> consumo = new java.util.LinkedHashMap<>();
        consumo.put("estado", "En observación");
        consumo.put("puntuacion", 58);
        consumo.put("indicadores", Map.of(
                "distribucion_gasto_categoria", Map.of(
                        "Vivienda", 30.2,
                        "Alimentación", 21.8,
                        "Transporte", 12.5,
                        "Salud", 4.8,
                        "Educación", 6.5,
                        "Entretenimiento y ocio", 15.4,
                        "Suscripciones digitales", 6.1,
                        "Compras personales", 2.7,
                        "Viajes y vacaciones", 0.0,
                        "Otros", 0.0
                ),
                "indice_concentracion", 0.58
        ));
        consumo.put("perfil_consumo", Map.of(
                "predominio_gasto", "Balance entre gastos esenciales y discrecionales",
                "tipo_consumo", "Moderadamente concentrado",
                "diversificacion_consumo", "Diversificado",
                "categoria_predominante", "Vivienda"
        ));
        consumo.put("recomendaciones", List.of(
                "Reducir gradualmente el gasto en entretenimiento.",
                "Mantener una distribución equilibrada entre gastos esenciales y discrecionales."
        ));

        Map<String, Object> dimensiones = new java.util.LinkedHashMap<>();
        dimensiones.put("balance_financiero", balance);
        dimensiones.put("capacidad_ahorro", ahorro);
        dimensiones.put("endeudamiento", endeudamiento);
        dimensiones.put("comportamiento_consumo", consumo);

        respuesta.put("dimensiones", dimensiones);

        respuesta.put("recomendaciones_generales", List.of(
                "Incrementar la capacidad de ahorro para fortalecer la estabilidad financiera.",
                "Mantener el bajo nivel de endeudamiento actual.",
                "Revisar periódicamente los gastos discrecionales para mejorar el margen financiero."
        ));

        return respuesta;
    }
}
