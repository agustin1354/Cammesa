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

        # Obtener datos de la API
        values = get_demand_comparison_values(region_id)

        current = values.get("current")
        yesterday = values.get("yesterday")
        last_week = values.get("last_week")
        timestamp = values.get("timestamp")
        history = values.get("history", [])

        print(f"[{region_id}] 🕒 Hora de medición seleccionada: {timestamp or 'No disponible'}")

        # Mostrar valores con seguridad ante None
        print(f"[{region_id}] 📊 Datos obtenidos:")
        print(f"[{region_id}]   Hoy: {f'{current:.1f} MW' if isinstance(current, (int, float)) else '❌ No disponible'}")
        print(f"[{region_id}]   Ayer: {f'{yesterday:.1f} MW' if isinstance(yesterday, (int, float)) else '❌ No disponible'}")
        print(f"[{region_id}]   Semana pasada: {f'{last_week:.1f} MW' if isinstance(last_week, (int, float)) else '❌ No disponible'}")

        # Solo detectar picos si los valores principales están disponibles
        if current is not None and yesterday is not None and last_week is not None:
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
                    f"🚨 ¡Alerta CAMMESA!\n\n"
                    f"Región: {region_name} (ID: {region_id})\n"
                    f"Hora: {timestamp}\n"
                    f"Valores:\n"
                    f"Hoy: {current:.1f} MW\n"
                    f"Ayer: {yesterday:.1f} MW\n"
                    f"Semana pasada: {last_week:.1f} MW\n"
                    f"Causas:\n" + "\n".join(reasons)
                )
                subject_email = f"⚠️ [ALERTA] Caída en Demanda [{region_name}]"

                try:
                    send_email(subject_email, mensaje_email)
                    print(f"[{region_id}] ✅ Correo enviado exitosamente")
                except Exception as e:
                    print(f"[{region_id}] ❌ Error enviando correo:", str(e))

                # Registrar alerta (opcional – desactiva esto si no usas el CSV)
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
                print(f"[{region_id}] ✅ No se detectaron picos")
                if len(reasons) > 0:
                    print(f"[{region_id}] ℹ️ Diferencias menores al umbral:")
                    for r in reasons:
                        print(f"[{region_id}]    - {r}")
        else:
            print(f"[{region_id}] ⚠️ Datos incompletos → omitiendo detección de picos")

if __name__ == "__main__":
    #test_write()  # Prueba de escritura
     job()       # Descomenta cuando sepas que funciona
