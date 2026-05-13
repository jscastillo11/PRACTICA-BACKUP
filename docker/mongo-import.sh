#!/bin/bash
set -euo pipefail
URI="mongodb://${MONGO_HOST:-mongo}:27017/agile_data_science"
FILE="${IMPORT_FILE:-/import/origin_dest_distances.jsonl}"

until mongosh "$URI" --eval "db.runCommand({ ping: 1 })" --quiet >/dev/null 2>&1; do
  echo "Esperando a Mongo..."
  sleep 2
done

COUNT=$(mongosh "$URI" --quiet --eval "db.origin_dest_distances.countDocuments()" | tr -d ' \r\n\t')
if [[ "${COUNT:-0}" -eq 0 ]]; then
  echo "Importando distancias..."
  mongoimport --uri "$URI" -c origin_dest_distances --file "$FILE"
  mongosh "$URI" --eval 'db.origin_dest_distances.createIndex({ Origin: 1, Dest: 1 })'
else
  echo "Colección origin_dest_distances ya tiene datos ($COUNT), omitiendo import."
fi
