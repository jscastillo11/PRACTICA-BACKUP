#!/bin/bash
set -euo pipefail

ICEBERG_VER="${ICEBERG_RUNTIME_VERSION:-1.5.2}"
HADOOP_AWS_VER="${HADOOP_AWS_VERSION:-3.3.4}"
AWS_BUNDLE_VER="${AWS_JAVA_BUNDLE_VERSION:-1.12.367}"

PACKAGES="org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:${ICEBERG_VER},org.apache.hadoop:hadoop-aws:${HADOOP_AWS_VER},com.amazonaws:aws-java-sdk-bundle:${AWS_BUNDLE_VER}"

exec "${SPARK_HOME}/bin/spark-submit" \
  --driver-memory "${SPARK_DRIVER_MEMORY:-2g}" \
  --packages "${PACKAGES}" \
  /app/ingest_training_to_iceberg.py "$@"
