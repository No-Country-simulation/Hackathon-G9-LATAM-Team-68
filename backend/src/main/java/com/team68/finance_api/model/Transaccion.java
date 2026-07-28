package com.team68.finance_api.model;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;


@Entity
@Table(name = "trasacciones")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Transaccion {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "usuario_id", nullable = false)
    private Usuario usuario;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal monto;

    @Column (nullable = false)
    private LocalDate fecha;

    @Column(nullable = false)
    private String descripcion;

    @Enumerated(EnumType.STRING)
    @Column (name = "tipo_financiero", nullable = false)
    private  TipoFinanciero tipoFinanciero;

    @Enumerated(EnumType.STRING)
    @Column (nullable = true)
    private CategoriaConsumo categoria;

    @Enumerated(EnumType.STRING)
    @Column(nullable = true)
    private GrupoCategoria grupo;

}
