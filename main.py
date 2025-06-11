# main.py

from data_fetcher import get_demand_comparison_values
from detector import check_peak
from notifier import send_email
from logger import log_alert
from config import THRESHOLD_DAILY, THRESHOLD_LAST_MEASUREMENT, REGIONS, CSV_FILE_PATH

import time
import schedule


def job():
    print("🔄 Iniciando revisión de todas las regiones...")
    
    for region_id, region_name in REGIONS.items():
        print(f"\n📶 Revisando región: {region_name} (ID: {region_id})...")

        # Obtener datos con historial completo
        values = get_demand_comparison_values(region_id)

        current = values.get("current")
        yesterday = values.get("yesterday")
        last_week = values.get("last_week")
        timestamp = values.get("timestamp")
        history = values.get("history", [])

        if current is None:
            print(f"[{region_id}] ❌ No se pudo obtener la demanda actual.")
            continue

        print(f"[{region_id}] 🕒 Hora de la medición seleccionada: {timestamp}")
        print(f"[{region_id}] 📊 Datos obtenidos:")
        print(f"[{region_id}]   Hoy: {current:.1f} MW")
        print(f"[{region_id}]   Ayer: {yesterday:.1f} MW")
        print(f"[{region_id}]   Semana pasada: {last_week:.1f} MW")

        # Llamar al detector con los nuevos parámetros
        is_peak, reasons = check_peak(
            current=current,
            yesterday=yesterday,
            last_week=last_week,
            history=history,
            threshold_daily=THRESHOLD_DAILY,
            threshold_last_measurement=THRESHOLD_LAST_MEASUREMENT
        )

        if is_peak:
            mensaje_email = (
                f"🚨 ¡Alerta de caída significativa en la demanda!\n\n"
                f"Región: {region_name} (ID: {region_id})\n"
                f"Hora de medición: {timestamp}\n"
                f"Valores:\n"
                f"Hoy: {current:.1f} MW\n"
                f"Ayer: {yesterday:.1f} MW\n"
                f"Semana pasada: {last_week:.1f} MW\n"
                f"Causas:\n" + "\n".join(reasons)
            )
            subject_email = f"⚠️ Alerta - Caída en Demanda [{region_name}]"
            try:
                send_email(subject_email, mensaje_email)
                print(f"[{region_id}] ✅ Correo enviado exitosamente")
            except Exception as e:
                print(f"[{region_id}] ❌ Error enviando correo:", str(e))

            # Registrar alerta (opcional – desactiva logger si no usas el CSV)
            log_alert(
                filepath=CSV_FILE_PATH,
                region_id=region_id,
                region_name=region_name,
                hoy=current,
                ayer=yesterday,
                semana_anterior=last_week,
                porcentaje_ayer=((yesterday - current) / yesterday * 100) if yesterday > 0 else 0,
                porcentaje_semana=((last_week - current) / last_week * 100) if last_week > 0 else 0
            )
        else:
            print(f"[{region_id}] ✅ No se detectaron picos o caídas significativas")
            if len(reasons) > 0:
                print(f"[{region_id}] ℹ️  Diferencias menores al umbral:")
                for r in reasons:
                    print(f"[{region_id}]    - {r}")

if __name__ == "__main__":
    #test_write()  # Prueba de escritura
     job()       # Descomenta cuando sepas que funciona
