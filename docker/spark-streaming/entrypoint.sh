#!/bin/bash
set -euo pipefail
exec "${SPARK_HOME}/bin/spark-submit" \
  --driver-memory "${SPARK_DRIVER_MEMORY:-2g}" \
  --packages "org.mongodb.spark:mongo-spark-connector_2.12:10.4.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3" \
  --class es.upm.dit.ging.predictor.MakePrediction \
  /app/flight_prediction.jar
