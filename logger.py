# logger.py

import csv
from datetime import datetime
import os

def init_log_file(filepath):
    """Crea el archivo CSV si no existe"""
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

def log_alert(filepath, **kwargs):
    """
    Guarda una nueva fila en el CSV
    """
    timestamp = kwargs.get("timestamp", datetime.now().isoformat())
    region_id = kwargs.get("region_id", "")
    region_name = kwargs.get("region_name", "")
    hoy = kwargs.get("hoy", "")
    ayer = kwargs.get("ayer", "")
    semana_anterior = kwargs.get("semana_anterior", "")
    porcentaje_ayer = ((ayer - hoy) / ayer) * 100 if ayer > 0 else 0
    porcentaje_semana = ((semana_anterior - hoy) / semana_anterior) * 100 if semana_anterior > 0 else 0

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
            f"{porcentaje_ayer:.1f}",
            f"{porcentaje_semana:.1f}"
        ])

    print(f"✅ Alerta registrada en {filepath}")
