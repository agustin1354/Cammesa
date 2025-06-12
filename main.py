# main.py

from data_fetcher import get_demand_comparison_values
from detector import check_peak
from notifier import send_email
from logger import log_alert
from config import THRESHOLD_DAILY, THRESHOLD_LAST_MEASUREMENT, REGIONS, CSV_FILE_PATH
from helpers import generate_alert_html
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

        if current is None:
            print(f"[{region_id}] ❌ No se pudo obtener la demanda actual.")
            continue

        print(f"[{region_id}] 🕒 Hora de medición seleccionada: {timestamp}")
        print(f"[{region_id}] 📊 Datos obtenidos:")
        print(f"[{region_id}]   Hoy: {f'{current:.1f} MW' if isinstance(current, (int, float)) else '❌ No disponible'}")
        print(f"[{region_id}]   Ayer: {f'{yesterday:.1f} MW' if isinstance(yesterday, (int, float)) else '❌ No disponible'}")
        print(f"[{region_id}]   Semana pasada: {f'{last_week:.1f} MW' if isinstance(last_week, (int, float)) else '❌ No disponible'}")

        # Solo detectar picos si todos los valores son válidos
        if yesterday is not None and last_week is not None and yesterday > 0 and last_week > 0:
            try:
                is_peak, reasons = check_peak(
                    current=current,
                    yesterday=yesterday,
                    last_week=last_week,
                    history=history,
                    threshold_daily=THRESHOLD_DAILY,
                    threshold_last_measurement=THRESHOLD_LAST_MEASUREMENT
                )

                if is_peak:
                    
                    ''' VERSION MENSAJE VIEJO
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
                    send_email(subject_email, mensaje_email)
                    '''

                    # Agregar umbrales actuales a las razones (opcional)
                    reasons.A_THRESHOLD = THRESHOLD_DAILY
                    reasons.B_THRESHOLD = THRESHOLD_LAST_MEASUREMENT
        
                    mensaje_html = generate_alert_html(
                        region_name=region_name,
                        region_id=region_id,
                        timestamp=timestamp,
                        current=current,
                        yesterday=yesterday,
                        last_week=last_week,
                        history=history,
                        reasons=reasons
                    )
                    subject_email = f"⚠️ [ALERTA] Caída significativa – {region_name}"
                    send_email(subject_email, mensaje_html)
                    
                else:
                    print(f"[{region_id}] ✅ No se detectaron picos")
                    if len(reasons) > 0:
                        print(f"[{region_id}] ℹ️ Diferencias menores al umbral:")
                        for r in reasons:
                            print(f"[{region_id}]    - {r}")
            except Exception as e:
                print(f"[{region_id}] ❌ Error al procesar alerta:", e)
        else:
            print(f"[{region_id}] ⚠️ Datos incompletos o cero → omitiendo detección")

if __name__ == "__main__":
    job()
