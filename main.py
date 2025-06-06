# main.py

from data_fetcher import get_demand_comparison_values
from detector import check_peak
from notifier import send_email
#from whatsapp_notifier import send_whatsapp_alert # Desactivado temporalmente
#from twilio.rest import Client
from config import THRESHOLD_PERCENTAGE, REGIONS
import time
import schedule
import csv
from io import StringIO
from logger import log_alert
from datetime import datetime

def job():
    print("🔄 Iniciando revisión de todas las regiones...")
    for region_id, region_name in REGIONS.items():
        print(f"\n📶 Revisando región: {region_name} (ID: {region_id})...")

        values = get_demand_comparison_values(region_id)
        current = values["current"]
        yesterday = values["yesterday"]
        last_week = values["last_week"]
        timestamp = values["timestamp"]

        if current is None:
            print(f"[{region_id}] ❌ No se pudo obtener la demanda actual.")
            continue

        print(f"[{region_id}] 🕒 Hora de la medición seleccionada: {timestamp}")
        print(f"[{region_id}] 📊 Datos obtenidos:")
        print(f"[{region_id}]   Hoy: {current:.1f} MW")
        print(f"[{region_id}]   Ayer: {yesterday:.1f} MW")
        print(f"[{region_id}]   Semana anterior: {last_week:.1f} MW")

        is_peak, reasons = check_peak(current, yesterday, last_week, THRESHOLD_PERCENTAGE)

        if is_peak:
            # Enviar por correo
            mensaje_email = (
                f"🚨 ¡Alerta de caída significativa en la demanda!\n\n"
                f"Región: {region_name} (ID: {region_id})\n"
                f"Hora de medición: {timestamp}\n"
                f"Valores:\n"
                f"Hoy: {current:.1f} MW\n"
                f"Ayer: {yesterday:.1f} MW\n"
                f"Semana pasada: {last_week:.1f} MW\n\n"
                f"Causas:\n" + "\n".join(reasons)
            )
            subject_email = f"⚠️ Alerta - Caída en Demanda [{region_name}] ({THRESHOLD_PERCENTAGE}% o más)"
            

            try:
                send_email(subject_email, mensaje_email)
                log_alert(
                filepath="Alertas CAMMESA.csv",
                region_id=region_id,
                region_name=region_name,
                hoy=current,
                ayer=yesterday,
                semana_anterior=last_week,
                porcentaje_ayer=((yesterday - current) / yesterday * 100),
                porcentaje_semana=((last_week - current) / last_week * 100),
                medio="email",
                estado="exitoso"
                )
            except Exception as e:
                log_alert(
                filepath="Alertas CAMMESA.csv",
                region_id=region_id,
                region_name=region_name,
                hoy=current,
                ayer=yesterday,
                semana_anterior=last_week,
                porcentaje_ayer=((yesterday - current) / yesterday * 100),
                porcentaje_semana=((last_week - current) / last_week * 100),
                medio="email",
                estado=f"fallido: {str(e)}"
                )
          
            '''
            # Enviar por WhatsApp
            try:
                send_whatsapp_alert(region_name, current, yesterday, last_week, timestamp)
            except Exception as e:
                print(f"[{region_id}] ❌ Error al enviar por WhatsApp: {e}")
            '''
        else:
            print(f"[{region_id}] ✅ No se detectaron picos.")
            if len(reasons) > 0:
                print(f"[{region_id}] ℹ️  Diferencias encontradas:")
                for r in reasons:
                    print(f"[{region_id}]    - {r}")

if __name__ == "__main__":
    job()  # Ejecutar una sola vez
