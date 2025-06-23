# test_alert_email.py

from helpers import generate_alert_html
from notifier import send_email
from config import THRESHOLDS, RAW_REGION_DATA
from datetime import datetime

# Datos ficticios para probar
region_name = "Santa Cruz"
region_id = 2542
current = 105.0
yesterday = 133.0
last_week = 143.0
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Historial ficticio (con medición inmediata anterior)
history = [
    {
        "fecha": "2025-06-04T05:40:00",
        "demHoy": current,
        "demAyer": yesterday,
        "demSemanaAnt": last_week
    },
    {
        "fecha": "2025-06-04T05:35:00",
        "demHoy": 129.0,  # Medición inmediata anterior
        "demAyer": 133.0,
        "demSemanaAnt": 143.0
    }
]

# Razones simuladas para condición A (caída vs Ayer y Semana pasada)
reasons = [
    f"Hoy ({current:.1f} MW) es <strong>{((yesterday - current) / yesterday * 100):.1f}%</strong> menor que Ayer",
    f"Hoy ({current:.1f} MW) es <strong>{((last_week - current) / last_week * 100):.1f}%</strong> menor que Semana Pasada"
]

print("🧪 Iniciando prueba de correo...")

try:
    mensaje_html = generate_alert_html(
        region_name=region_name,
        region_id=region_id,
        timestamp=timestamp,
        current=current,
        yesterday=yesterday,
        last_week=last_week,
        history=history,
        reasons=reasons,
        a_threshold=THRESHOLDS["PROVINCIA"]["THRESHOLD_DAILY"],
        b_threshold=THRESHOLDS["PROVINCIA"]["THRESHOLD_LAST_MEASUREMENT"],
        level="PROVINCIA"
    )

    subject = f"⚠️ [PRUEBA] Alerta CAMMESA – {region_name}"

    send_email(subject, mensaje_html)

    print("✅ Correo de prueba generado y enviado")
except Exception as e:
    print(f"❌ Se produjo una excepción: {e}")
