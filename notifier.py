# notifier.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    from config import EMAIL_FROM, EMAIL_PASSWORD, EMAIL_ALERT_TO

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_ALERT_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_ALERT_TO, text)
        print("✅ Correo enviado exitosamente.")
    except Exception as e:
        print(f"❌ Error enviando correo: {e}")
    finally:
        server.quit()