# test_alert_email.py

from helpers import generate_alert_html
from notifier import send_email
import json
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

# Razones simuladas para condición A
reasons = [
    f"Hoy ({current:.1f} MW) es <strong>{((yesterday - current) / yesterday * 100):.1f}%</strong> menor que Ayer ({yesterday:.1f} MW)",
    f"Hoy ({current:.1f} MW) es <strong>{((last_week - current) / last_week * 100):.1f}%</strong> menor que Semana pasada ({last_week:.1f} MW)"
]

print("🧪 Generando correo de prueba...")

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

subject = "⚠️ [PRUEBA] Alerta CAMMESA – Caída en Demanda"

send_email(subject, mensaje_html)

print("✅ Correo de prueba generado y enviado")
