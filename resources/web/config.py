# config.py, a configuration file for index.py
import os

RECORDS_PER_PAGE=15
AIRPLANE_RECORDS_PER_PAGE=5
ELASTIC_URL = os.environ.get(
    "ELASTIC_URL",
    "http://localhost:9200/agile_data_science",
)
