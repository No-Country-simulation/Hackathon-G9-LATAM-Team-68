package com.team68.finance_api.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "medallas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Medalla {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String codigo; // ej: "AHORRADOR_BRONCE", "DEUDA_ZERO"

    private String nombre;
    private String descripcion;
    private String iconoUrl;
    private Integer puntos;
}