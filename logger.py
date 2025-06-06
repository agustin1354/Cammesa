# logger.py

import csv
from datetime import datetime
import os

def log_alert(filepath="C:\Users\difilippoa\OneDrive - Telefonica\Seguimiento Contratistas - Gestiones Proveedores de Energía\Alertas CAMMESA.csv", **kwargs):
    timestamp = kwargs.get("timestamp", datetime.now().isoformat())
    region_id = kwargs.get("region_id", "")
    region_name = kwargs.get("region_name", "")
    hoy = kwargs.get("hoy", "")
    ayer = kwargs.get("ayer", "")
    semana_anterior = kwargs.get("semana_anterior", "")
    porcentaje_ayer = kwargs.get("porcentaje_ayer", "")
    porcentaje_semana = kwargs.get("porcentaje_semana", "")

    # Verificar si el archivo ya existe
    file_exists = os.path.exists(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
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

    print(f"✅ Alerta guardada en {filepath}")
