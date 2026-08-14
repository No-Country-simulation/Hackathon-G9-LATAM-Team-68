package com.team68.finance_api.service;

import com.team68.finance_api.dto.request.AnalisisRequestDTO;
import com.team68.finance_api.dto.response.AnalisisResponseDTO;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class CalculoFinancieroService {

    @Value("${analisis.api.url}")
    private String analisisApiUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public AnalisisResponseDTO calcularAnalisisFinanciero(AnalisisRequestDTO request) {
        // Limpia la barra diagonal final si la hubiera y concatena el endpoint /analizar
        String url = analisisApiUrl.replaceAll("/+$", "") + "/analizar";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<AnalisisRequestDTO> entity = new HttpEntity<>(request, headers);

        ResponseEntity<AnalisisResponseDTO> response = restTemplate.postForEntity(
                url,
                entity,
                AnalisisResponseDTO.class
        );

        return response.getBody();
    }
}