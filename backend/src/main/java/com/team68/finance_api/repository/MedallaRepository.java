package com.team68.finance_api.repository;

import com.team68.finance_api.model.Medalla;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface MedallaRepository extends JpaRepository<Medalla, Long> {
    Optional<Medalla> findByCodigo(String codigo);
}