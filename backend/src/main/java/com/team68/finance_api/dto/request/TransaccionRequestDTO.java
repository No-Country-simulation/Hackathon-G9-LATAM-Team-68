package com.team68.finance_api.dto.request;

import com.team68.finance_api.model.*;
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


    @NotNull(message = "El monto es obligatorio")
    @Positive(message = "El monto debe ser un valor positivo")
    private BigDecimal monto;

    @NotNull(message = "La fecha de la transacción es obligatoria")
    private LocalDate fecha;

    @NotBlank(message = "La descripción no puede estar vacía")
    private String descripcion;


    private TipoFinanciero tipoFinanciero;

    private CategoriaConsumo categoria;

    @NotNull(message = "El método de pago es obligatorio")
    private MetodoPago metodoPago;


    private BigDecimal tasaInteresTarjeta;

}
