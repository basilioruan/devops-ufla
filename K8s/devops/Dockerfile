# Estágio de Build: (Mudei para a tag 'jdk' em vez de 'jdk-alpine' para evitar problemas de dependência do builder)
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
RUN ./mvnw dependency:go-offline
COPY src src
RUN ./mvnw package -DskipTests

# Estágio de Execução: Cria a imagem final leve
# CORREÇÃO AQUI: Usando a tag JRE oficial do Temurin para uma base Debian (padrão)
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]