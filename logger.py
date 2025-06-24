# logger.py

import csv
from datetime import datetime
import os

def log_measurement(filepath="mediciones.csv", **kwargs):
    timestamp_medicion = kwargs.get("timestamp", "")
    region_id = kwargs.get("region_id", "")
    region_name = kwargs.get("region_name", "")
    current = kwargs.get("hoy", "")
    yesterday = kwargs.get("ayer", "")
    last_week = kwargs.get("semana_anterior", "")
    level = kwargs.get("nivel_alerta", "NINGUNA")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ Marca única por ejecución
    porcentaje_ayer = ((yesterday - current) / yesterday * 100) if yesterday and current else 0
    porcentaje_semana = ((last_week - current) / last_week * 100) if last_week and current else 0

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
            current,
            yesterday,
            last_week,
            f"{porcentaje_ayer:.1f}",
            f"{porcentaje_semana:.1f}",
            level
        ])

    print(f"✅ Medición registrada – {now}")
