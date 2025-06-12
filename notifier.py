# notifier.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_FROM, EMAIL_PASSWORD, EMAIL_ALERT_TO


def send_email(subject, body_html):
    """
    Envía un correo con formato HTML
    """
    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_ALERT_TO
    msg['Subject'] = subject

    # Adjuntar contenido HTML
    msg.attach(MIMEText(body_html, "html"))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_ALERT_TO, msg.as_string())
        print("✅ Correo enviado exitosamente.")
    except Exception as e:
        print(f"❌ Error enviando correo: {e}")
    finally:
        server.quit()
