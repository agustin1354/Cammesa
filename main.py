# main.py

from data_fetcher import get_demand_comparison_values
from detector import check_peak
from notifier import send_email
from logger import log_alert
from config import THRESHOLDS, REGIONS, CSV_FILE_PATH
from utils import get_region_level
from datetime import datetime


def job():
    print("🔄 Iniciando revisión de todas las regiones...")

    for region_id, region_name in REGIONS.items():
        print(f"\n📶 Revisando región: {region_name} (ID: {region_id})...")

        values = get_demand_comparison_values(region_id)

        current = values.get("current")
        yesterday = values.get("yesterday")
        last_week = values.get("last_week")
        timestamp = values.get("timestamp")
        history = values.get("history", [])

        if current is None or yesterday is None or last_week is None:
            print(f"[{region_id}] ❌ Datos incompletos → omitiendo alerta")
            continue

        # Obtener el nivel de la región
        level = get_region_level(region_id, RAW_REGION_DATA)

        # Asignar umbrales según nivel
        threshold_daily = THRESHOLDS[level]["THRESHOLD_DAILY"]
        threshold_last_measurement = THRESHOLDS[level]["THRESHOLD_LAST_MEASUREMENT"]

        # Detectar alerta
        is_peak, reasons = check_peak(
            current=current,
            yesterday=yesterday,
            last_week=last_week,
            history=history,
            threshold_daily=threshold_daily,
            threshold_last_measurement=threshold_last_measurement
        )

        if is_peak:
            print(f"[{region_id}] ⚠️ Alerta disparada ({level})")

            mensaje_html = generate_alert_html(
                region_name=region_name,
                region_id=region_id,
                timestamp=timestamp,
                current=current,
                yesterday=yesterday,
                last_week=last_week,
                history=history,
                reasons=reasons,
                a_threshold=threshold_daily,
                b_threshold=threshold_last_measurement,
                level=level
            )
            subject_email = f"⚠️ [ALERTA] Caída significativa – {region_name}"

            try:
                send_email(subject_email, mensaje_html)
                print(f"[{region_id}] ✅ Correo enviado correctamente")
            except Exception as e:
                print(f"[{region_id}] ❌ Error al enviar correo: {e}")

        else:
            print(f"[{region_id}] ✅ No hay alerta")

if __name__ == "__main__":
    job()
