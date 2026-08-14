package com.team68.finance_api.controller;

import com.team68.finance_api.dto.request.SolicitudAnalisisDTO;
import com.team68.finance_api.dto.response.AnalisisResponseDTO;
import com.team68.finance_api.service.CalculoFinancieroService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/analisis") // Ajusta el path según tu ruta configurada
public class AnalisisController {

    private final CalculoFinancieroService calculoFinancieroService;

    public AnalisisController(CalculoFinancieroService calculoFinancieroService) {
        this.calculoFinancieroService = calculoFinancieroService;
    }

    @PostMapping("/analizar")
    public ResponseEntity<AnalisisResponseDTO> analizar(@Valid @RequestBody SolicitudAnalisisDTO solicitud) {
        AnalisisResponseDTO respuesta = calculoFinancieroService.calcularAnalisisFinanciero(solicitud);
        return ResponseEntity.ok(respuesta);
    }
}