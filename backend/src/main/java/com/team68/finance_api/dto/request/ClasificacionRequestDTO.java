package com.team68.finance_api.dto.request;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ClasificacionRequestDTO {
    private UsuarioRequestDTO usuario;
    private List<TransaccionRequestDTO> transacciones;
}