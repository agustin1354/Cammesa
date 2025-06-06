# logger.py

import csv
from datetime import datetime
import os


def init_log_file(filepath="alertas.csv"):
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "region_id",
                "region_name",
                "hoy",
                "ayer",
                "semana_anterior",
                "porcentaje_ayer",
                "porcentaje_semana"
            ])
        print(f"✅ Archivo {filepath} creado")
    else:
        print(f"ℹ️  Archivo {filepath} ya existe")


def log_alert(filepath="alertas.csv", **kwargs):
    timestamp = kwargs.get("timestamp", datetime.now().isoformat())
    region_id = kwargs.get("region_id", "")
    region_name = kwargs.get("region_name", "")
    hoy = kwargs.get("hoy", "")
    ayer = kwargs.get("ayer", "")
    semana_anterior = kwargs.get("semana_anterior", "")
    porcentaje_ayer = kwargs.get("porcentaje_ayer", "")
    porcentaje_semana = kwargs.get("porcentaje_semana", "")

    init_log_file(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            region_id,
            region_name,
            hoy,
            ayer,
            semana_anterior,
            porcentaje_ayer,
            porcentaje_semana
        ])

    print(f"✅ Alerta registrada en {filepath}")
