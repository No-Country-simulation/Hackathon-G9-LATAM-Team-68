package com.team68.finance_api.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
public class ClasificacionTransaccionesController {

    @PostMapping("/clasificacion-transacciones")
    public Map<String, Object> clasificar (@RequestBody Map<String, Object> entrada){
        return Map.of(
                "tipo", "CONSUMO",
                "categoria", "Alimentación"
        );
    }

}
