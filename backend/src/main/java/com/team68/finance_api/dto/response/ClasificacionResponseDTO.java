package com.team68.finance_api.dto.response;

import com.team68.finance_api.model.CategoriaConsumo;
import com.team68.finance_api.model.GrupoCategoria;
import com.team68.finance_api.model.TipoFinanciero;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClasificacionResponseDTO {

    private TipoFinanciero tipoFinanciero;
    private CategoriaConsumo categoriaAsignada;
    private GrupoCategoria grupo;

}
