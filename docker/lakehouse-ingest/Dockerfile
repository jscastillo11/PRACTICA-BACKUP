# Spark 3.5.3 + PySpark + job de ingesta a Iceberg sobre MinIO (S3A)
FROM eclipse-temurin:17-jdk-jammy

ARG SPARK_VERSION=3.5.3
ARG SPARK_HADOOP=3
ENV SPARK_HOME=/opt/spark \
    PATH="${PATH}:/opt/spark/bin" \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl python3 python3-pip procps \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP}.tgz" \
    | tar -xz -C /opt \
    && mv "/opt/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP}" /opt/spark \
    && pip3 install --no-cache-dir "pyspark==${SPARK_VERSION}"

COPY resources/ingest_training_to_iceberg.py /app/ingest_training_to_iceberg.py
COPY docker/lakehouse-ingest/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
