package com.team68.finance_api.repository;

import com.team68.finance_api.model.Transaccion;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public interface TransaccionRepository extends JpaRepository<Transaccion, UUID> {

    List<Transaccion> findByUsuarioId(UUID usuarioId);

    // Obtener transacciones por usuario y rango de fechas (Periodo)
    List<Transaccion> findByUsuarioIdAndFechaBetween(UUID usuarioId, LocalDate inicio, LocalDate fin);
}