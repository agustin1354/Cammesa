# test_write.py

import csv
from datetime import datetime
import os

# Ruta donde quieres guardar el archivo
CSV_FILE_PATH = r"C:\Users\difilippoa\OneDrive - Telefonica\Seguimiento Contratistas - Gestiones Proveedores de Energía\test_alertas.csv"

print(f"📝 Probando escritura en: {CSV_FILE_PATH}")

try:
    # Crear la carpeta si no existe
    os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)

    # Escribir en el archivo CSV
    file_exists = os.path.exists(CSV_FILE_PATH)

    with open(CSV_FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            # Escribir encabezado solo si es nuevo
            writer.writerow([
                "timestamp",
                "region_id",
                "region_name",
                "hoy",
                "ayer",
                "semana_anterior"
            ])

        # Escribir datos de prueba
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            1002,
            "Total SADI",
            14000,
            18000,
            17500
        ])

    print("✅ Archivo CSV creado o actualizado correctamente")
    print("📁 Ubicación:", CSV_FILE_PATH)

except Exception as e:
    print("❌ Error al escribir archivo:", e)
