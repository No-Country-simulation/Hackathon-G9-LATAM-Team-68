# 1. Imagen base con Java 17 y Maven para compilar el proyecto
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

# Copiar el código fuente y el pom.xml
COPY . .

# Compilar la aplicación omitiendo las pruebas para agilizar
RUN chmod +x mvnw
RUN ./mvnw clean package -DskipTests

# 2. Imagen ligera solo con el Runtime de Java para ejecutar el JAR
FROM eclipse-temurin:17-jre
WORKDIR /app

# Copiar el archivo .jar generado desde la etapa de compilación
COPY --from=build /app/target/*.jar app.jar

# Puerto donde corre Spring Boot
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "java -jar app.jar --server.port=${PORT}"]

# Comando para iniciar la aplicación
ENTRYPOINT ["java", "-jar", "app.jar"]