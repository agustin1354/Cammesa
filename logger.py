# logger.py

import csv
from datetime import datetime
import os


def init_log_file(filepath="Alertas CAMMESA.csv"):
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
                "porcentaje_hoy_ayer",
                "porcentaje_hoy_semana",
                "medio",
                "estado"
            ])
        print("✅ Archivo de log creado:", filepath)


def log_alert(filepath="Alertas CAMMESA.csv", **kwargs):
    """
    Guarda una alerta en el archivo CSV
    """
    timestamp = kwargs.get("timestamp", datetime.now().isoformat())
    region_id = kwargs.get("region_id", "")
    region_name = kwargs.get("region_name", "")
    hoy = kwargs.get("hoy", "")
    ayer = kwargs.get("ayer", "")
    semana_anterior = kwargs.get("semana_anterior", "")
    porcentaje_ayer = kwargs.get("porcentaje_ayer", "")
    porcentaje_semana = kwargs.get("porcentaje_semana", "")
    medio = kwargs.get("medio", "")
    estado = kwargs.get("estado", "")

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
            porcentaje_semana,
            medio,
            estado
        ])
    print(f"✅ Alerta registrada en {filepath}")
