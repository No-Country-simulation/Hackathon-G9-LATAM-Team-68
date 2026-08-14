package com.team68.finance_api.dto.request;

import com.team68.finance_api.model.CategoriaConsumo;
import com.team68.finance_api.model.TipoFinanciero;
import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TransaccionRequestDTO {
    @NotNull(message = "La fecha es obligatoria")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    private LocalDate fecha;

    @NotBlank(message = "La descripción no puede estar vacía")
    private String descripcion;

    @NotNull(message = "El monto es obligatorio")
    @Positive(message = "El monto debe ser positivo")
    private BigDecimal monto;

    @JsonProperty("forma_pago")
    @JsonAlias("formaPago") // Acepta tanto forma_pago como formaPago
    private String formaPago;

    @JsonProperty("tasa_de_interes_de_la_tarjeta")
    @JsonAlias("tasaDeInteresDeLaTarjeta")
    private Double tasaDeInteresDeLaTarjeta;
}