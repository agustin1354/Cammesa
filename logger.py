# logger.py

import csv
from datetime import datetime
import os

def log_measurement(filepath="mediciones.csv", **kwargs):
    timestamp_medicion = kwargs.get("timestamp", "")
    region_id = kwargs.get("region_id", "")
    region_name = kwargs.get("region_name", "")
    current = kwargs.get("hoy", "")
    previous_measurement = kwargs.get("anterior", "")
    yesterday = kwargs.get("ayer", "")
    last_week = kwargs.get("semana_anterior", "")
    level = kwargs.get("nivel_alerta", "NINGUNA")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ Marca única por ejecución
    file_exists = os.path.exists(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp_registro",
                "timestamp_medición",
                "region_id",
                "region_name",
                "hoy",
                "anterior",
                "ayer",
                "semana_anterior",
                "porcentaje_ayer",
                "porcentaje_semana",
                "nivel_alerta"
            ])
        writer.writerow([
            now,
            timestamp_medicion,
            region_id,
            region_name,
            f"{current:.1f}" if current else "",
            f"{previous_measurement:.1f}" if previous_measurement else "",
            f"{yesterday:.1f}" if yesterday else "",
            f"{last_week:.1f}" if last_week else "",
            f"{((yesterday - current) / yesterday * 100):.1f}" if yesterday and current else "",
            f"{((last_week - current) / last_week * 100):.1f}" if last_week and current else "",
            level
        ])

    print(f"✅ Medición registrada – {now} | {region_name}")
