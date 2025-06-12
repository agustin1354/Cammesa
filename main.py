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
                    send_email_alert(subject_email, mensaje_html)
                    
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

    def generate_alert_html(region_name, region_id, timestamp, current, yesterday, last_week, history, reasons):
    valid_history = [r for r in history if float(r.get("demHoy", 0)) > 0]
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h1 style="color:#D32F2F;">🚨 ¡Alerta CAMMESA!</h1>
        <p>Se ha detectado una caída significativa en la demanda eléctrica.</p>

        <hr style="margin: 20px 0;">

        <h2 style="color:#3F51B5;">📌 Configuración actual de alertas:</h2>
        <ul>
            <li><strong>A)</strong> Hoy es ≥<strong>{SHOW_THRESHOLD_A}%</strong> menor que Ayer y Semana pasada</li>
            <li><strong>B)</strong> Hoy es ≥<strong>{SHOW_THRESHOLD_B}%</strong> menor que la medición inmediata anterior</li>
        </ul>

        <h2 style="color:#3F51B5;">📍 Región: {region_name} (ID: {region_id})</h2>
        <p><strong>Hora:</strong> {timestamp}</p>
        
        <h2 style="color:#3F51B5;">📊 Valores registrados</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #FFEBEE;">
                <th style="text-align:left;">Medición</th>
                <th style="text-align:right;">Demanda (MW)</th>
                <th style="text-align:center;">Fecha / Hora</th>
            </tr>
"""

    # Mostrar solo datos relevantes según condición
    if reasons and any("menor que Ayer" in r for r in reasons):
        fecha_hoy = timestamp
        fecha_ayer = "última medición"
        fecha_semana = "última medición"

        html += f"""
            <tr>
                <td>Hoy</td>
                <td style="text-align:right; color:red; font-weight:bold;">{current:.1f} MW</td>
                <td style="text-align:center;">{fecha_hoy.split()[1]} hs</td>
            </tr>
            <tr>
                <td>Ayer</td>
                <td style="text-align:right;">{yesterday:.1f} MW</td>
                <td style="text-align:center;">{fecha_ayer}</td>
            </tr>
            <tr>
                <td>Semana pasada</td>
                <td style="text-align:right;">{last_week:.1f} MW</td>
                <td style="text-align:center;">{fecha_semana}</td>
            </tr>
        """
    elif reasons and any("medición inmediata" in r for r in reasons):
        record = valid_history[-2]
        prev_fecha = record.get("fecha").split("T")[1].split(".")[0] if record.get("fecha") else "N/A"

        html += f"""
            <tr>
                <td>Hoy</td>
                <td style="text-align:right; color:red; font-weight:bold;">{current:.1f} MW</td>
                <td style="text-align:center;">{timestamp.split()[1]} hs</td>
            </tr>
            <tr>
                <td>Medición inmediata anterior</td>
                <td style="text-align:right;">{record["demHoy"]} MW</td>
                <td style="text-align:center;">{prev_fecha}</td>
            </tr>
        """

    html += """
        </table>

        <h2 style="color:#3F51B5;">🔍 Causa de la alerta</h2>
        <ul>
    """

    for razon in reasons:
        html += f"<li>{razon}</li>"

    html += """
        </ul>

        <p style="font-style: italic; color: #555;">Este aviso fue generado automáticamente según las condiciones definidas.</p>
    </body></html>
    """

    return html
