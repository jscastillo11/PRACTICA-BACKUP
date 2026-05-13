# Etapa 1: compilar el JAR con sbt (Scala 2.12)
FROM eclipse-temurin:17-jdk-jammy AS builder
ARG SBT_VERSION=1.10.7
ENV PATH="/opt/sbt/bin:${PATH}"
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz" \
    | tar xz -C /opt
WORKDIR /build
COPY flight_prediction /build/flight_prediction
WORKDIR /build/flight_prediction
RUN sbt -batch package

# Etapa 2: Spark precompilado + job de streaming
FROM eclipse-temurin:17-jdk-jammy
ARG SPARK_VERSION=3.5.3
ARG SPARK_HADOOP=3
ENV SPARK_HOME=/opt/spark \
    PATH="${PATH}:/opt/spark/bin"

RUN apt-get update && apt-get install -y --no-install-recommends curl procps \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP}.tgz" \
    | tar -xz -C /opt \
    && mv "/opt/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP}" /opt/spark

COPY --from=builder /build/flight_prediction/target/scala-2.12/flight_prediction_2.12-0.1.jar /app/flight_prediction.jar
COPY docker/spark-streaming/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
