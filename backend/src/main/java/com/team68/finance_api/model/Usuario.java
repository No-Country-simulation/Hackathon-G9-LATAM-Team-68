package com.team68.finance_api.model;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "usuarios")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password; // Encriptada con BCrypt

    private String nombre;
    private String email;
    private BigDecimal ingresoMensual;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "usuario_medallas",
        joinColumns = @JoinColumn(name = "usuario_id"),
        inverseJoinColumns = @JoinColumn(name = "medalla_id")
    )
    @Builder.Default
    private Set<Medalla> medallas = new HashSet<>();
}