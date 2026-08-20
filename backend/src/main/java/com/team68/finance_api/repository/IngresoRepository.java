package com.team68.finance_api.repository;

import com.team68.finance_api.model.Ingreso;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public interface IngresoRepository extends JpaRepository<Ingreso, UUID> {
    List<Ingreso> findByUsuarioId(UUID usuarioId);
    List<Ingreso> findByUsuarioIdAndFechaBetween(UUID usuarioId, LocalDate fechaInicio, LocalDate fechaFin);
}
