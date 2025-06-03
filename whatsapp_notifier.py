# whatsapp_notifier.py

from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, WHATSAPP_TO


def send_whatsapp_alert(region_name, current, yesterday, last_week, timestamp):
    """
    Envía una alerta por WhatsApp con formato simple
    """
    message_body = (
        f"🚨 *Alerta de caída significativa en la demanda*\n\n"
        f"📍 Región: {region_name}\n"
        f"🕒 Hora de medición: {timestamp}\n"
        f"📉 Hoy: {current:.1f} MW\n"
        f"📅 Ayer: {yesterday:.1f} MW\n"
        f"📆 Semana pasada: {last_week:.1f} MW\n\n"
        f"⚠️ Hoy es:\n"
        f"- {((yesterday - current) / yesterday * 100):.1f}% menor que Ayer\n"
        f"- {((last_week - current) / last_week * 100):.1f}% menor que Semana Pasada"
    )

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_FROM,
            to=WHATSAPP_TO
        )
        print(f"✅ Mensaje de WhatsApp enviado (SID: {message.sid})")
    except Exception as e:
        print(f"❌ Error enviando mensaje por WhatsApp: {e}")