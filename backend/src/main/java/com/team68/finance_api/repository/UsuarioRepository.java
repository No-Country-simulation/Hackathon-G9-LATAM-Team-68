package com.team68.finance_api.repository;

import com.team68.finance_api.model.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;
import java.util.UUID;

public interface UsuarioRepository extends JpaRepository<Usuario, UUID> {
    Optional<Usuario> findByUsername(String username);

    @Query("SELECT u FROM Usuario u LEFT JOIN FETCH u.medallas WHERE u.id = :id")
    Optional<Usuario> findByIdWithMedallas(@Param("id") UUID id);

    @Query("SELECT u FROM Usuario u LEFT JOIN FETCH u.medallas WHERE u.username = :username")
    Optional<Usuario> findByUsernameWithMedallas(@Param("username") String username);
}