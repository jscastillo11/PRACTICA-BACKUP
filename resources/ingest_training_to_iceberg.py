#!/usr/bin/env python3
"""
Carga datos de entrenamiento (mismo esquema que train_spark_mllib_model.py) en una
tabla Iceberg almacenada en MinIO (S3A). Punto 1 rúbrica Parte II GISD.
"""
import os
import sys


def main() -> None:
    base = os.environ.get("PRACTICA_DATA_DIR", "/opt/practica/data")
    bz2_path = os.path.join(base, "simple_flight_delay_features.jsonl.bz2")
    jsonl_path = os.path.join(base, "simple_flight_delay_features.jsonl")
    if os.path.isfile(bz2_path):
        input_path = bz2_path
    elif os.path.isfile(jsonl_path):
        input_path = jsonl_path
    else:
        print(
            "ERROR: No se encontró el dataset de entrenamiento.\n"
            f"  Coloca en ./data (montado en {base}) uno de:\n"
            "  - simple_flight_delay_features.jsonl.bz2  (recomendado, igual que el entrenamiento)\n"
            "  - simple_flight_delay_features.jsonl",
            file=sys.stderr,
        )
        sys.exit(2)

    minio_endpoint = os.environ.get("MINIO_ENDPOINT", "http://minio:9000").rstrip("/")
    bucket = os.environ.get("S3_WAREHOUSE_BUCKET", "lakehouse")
    access = os.environ.get("MINIO_ROOT_USER", "minioadmin")
    secret = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")
    catalog = os.environ.get("ICEBERG_CATALOG_NAME", "lakehouse")
    full_table = os.environ.get(
        "ICEBERG_TRAINING_TABLE", f"{catalog}.flights.training_features"
    )

    import pyspark.sql
    from pyspark.sql.types import (
        DateType,
        DoubleType,
        IntegerType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )

    schema = StructType(
        [
            StructField("ArrDelay", DoubleType(), True),
            StructField("CRSArrTime", TimestampType(), True),
            StructField("CRSDepTime", TimestampType(), True),
            StructField("Carrier", StringType(), True),
            StructField("DayOfMonth", IntegerType(), True),
            StructField("DayOfWeek", IntegerType(), True),
            StructField("DayOfYear", IntegerType(), True),
            StructField("DepDelay", DoubleType(), True),
            StructField("Dest", StringType(), True),
            StructField("Distance", DoubleType(), True),
            StructField("FlightDate", DateType(), True),
            StructField("FlightNum", StringType(), True),
            StructField("Origin", StringType(), True),
        ]
    )

    warehouse = f"s3a://{bucket}/warehouse"

    spark = (
        pyspark.sql.SparkSession.builder.appName("ingest_training_to_iceberg")
        .master("local[*]")
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
        )
        .config(f"spark.sql.catalog.{catalog}", "org.apache.iceberg.spark.SparkCatalog")
        .config(f"spark.sql.catalog.{catalog}.type", "hadoop")
        .config(f"spark.sql.catalog.{catalog}.warehouse", warehouse)
        .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.access.key", access)
        .config("spark.hadoop.fs.s3a.secret.key", secret)
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config(
            "spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print(f"Leyendo: {input_path}")
    df = spark.read.schema(schema).json(input_path)
    n = df.count()
    if n == 0:
        print("ERROR: El dataset está vacío.", file=sys.stderr)
        sys.exit(3)
    print(f"Filas leídas: {n}")

    ns = ".".join(full_table.split(".")[:2])
    spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {ns}")

    print(f"Escribiendo tabla Iceberg: {full_table} (warehouse={warehouse})")
    df.writeTo(full_table).using("iceberg").createOrReplace()

    spark.table(full_table).show(3, truncate=False)
    meta = spark.sql(f"DESCRIBE TABLE EXTENDED {full_table}").take(20)
    print("DESCRIBE TABLE EXTENDED (extracto):")
    for row in meta:
        print(row)

    spark.stop()
    print("Ingesta Iceberg completada.")


if __name__ == "__main__":
    main()
