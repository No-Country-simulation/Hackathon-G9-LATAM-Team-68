package com.team68.finance_api.controller;

import com.team68.finance_api.dto.request.AnalisisRequestDTO;
import com.team68.finance_api.dto.response.AnalisisResponseDTO;
import com.team68.finance_api.service.CalculoFinancieroService;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/analisis")
@CrossOrigin(origins = "*")
public class AnalisisController {

    private final CalculoFinancieroService calculoFinancieroService;

    public AnalisisController(CalculoFinancieroService calculoFinancieroService) {
        this.calculoFinancieroService = calculoFinancieroService;
    }

    @PostMapping
    public ResponseEntity<AnalisisResponseDTO> realizarAnalisis(@Valid @RequestBody AnalisisRequestDTO request) {
        AnalisisResponseDTO response = calculoFinancieroService.calcularAnalisisFinanciero(request);
        return ResponseEntity.ok(response);
    }
}
