package com.team68.finance_api.config;

import com.team68.finance_api.model.Medalla;
import com.team68.finance_api.repository.MedallaRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {

    private final MedallaRepository medallaRepository;

    public DataInitializer(MedallaRepository medallaRepository) {
        this.medallaRepository = medallaRepository;
    }

    @Override
    public void run(String... args) {
        if (medallaRepository.count() == 0) {
            medallaRepository.saveAll(List.of(
                // Permanentes
                Medalla.builder().codigo("PEQUENO_OSEZNO").nombre("Pequeño osezno").descripcion("Has iniciado sesión y creado una cuenta.").puntos(50).iconoUrl("/assets/osezno.png").build(),
                Medalla.builder().codigo("PRIMERA_PRIMAVERA").nombre("Primera Primavera").descripcion("Llevas racha de uso de la aplicación por un mes.").puntos(100).iconoUrl("/assets/primavera.png").build(),
                Medalla.builder().codigo("PREPARANDOTE_INVIERNO").nombre("Preparándote para el invierno").descripcion("Llevas racha de uso de la aplicación por 6 meses.").puntos(300).iconoUrl("/assets/invierno.png").build(),
                Medalla.builder().codigo("LETARGO_INVERNAL").nombre("Letargo invernal").descripcion("Tu aplicación no ha recibido actualizaciones por 1 mes.").puntos(0).iconoUrl("/assets/letargo.png").build(),

                // Mensuales
                Medalla.builder().codigo("A_LA_GARRA_CREDITO").nombre("A la garra con tu crédito").descripcion("Mantienes una constante de balance superior a tu mes anterior.").puntos(150).iconoUrl("/assets/garra_credito.png").build(),
                Medalla.builder().codigo("RECOLECTOR_MIEL").nombre("Recolector de Miel").descripcion("Llevas aumentando tus ingresos durante 3 semanas seguidas.").puntos(150).iconoUrl("/assets/recolector_miel.png").build(),
                Medalla.builder().codigo("HIBERNACION_MONETARIA").nombre("Hibernación monetaria").descripcion("Tus gastos no han subido durante el balance del último mes.").puntos(150).iconoUrl("/assets/hibernacion.png").build(),
                Medalla.builder().codigo("TREPANDO_CASCADA").nombre("Trepando la cascada").descripcion("Has mejorado tu puntuación financiera en un 25% a tu inicio de mes.").puntos(200).iconoUrl("/assets/cascada.png").build(),
                Medalla.builder().codigo("SALMON_DORADO").nombre("Salmón dorado").descripcion("Has conseguido números positivos durante los primeros 20 días del mes.").puntos(200).iconoUrl("/assets/salmon.png").build()
            ));
        }
    }
}