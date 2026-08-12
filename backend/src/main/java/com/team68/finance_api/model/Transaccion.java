package com.team68.finance_api.model;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonIgnore;

@Entity
@Table(name = "transacciones")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
public class Transaccion {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "usuario_id", nullable = false)
    @JsonIgnore
    private Usuario usuario;

    @Column(nullable = false)
    private LocalDate fecha;

    @Column(nullable = false)
    private String descripcion;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal monto;

    @Column(name = "forma_pago", nullable = false)
    private String formaPago;

    @Column(name = "tasa_interes")
    private Double tasaDeInteresDeLaTarjeta;

    @Enumerated(EnumType.STRING)
    @Column(name = "tipo_financiero")
    private TipoFinanciero tipoFinanciero;

    @Enumerated(EnumType.STRING)
    private CategoriaConsumo categoria;

    @Column(nullable = false)
    private Boolean esIngreso;
}