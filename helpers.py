# helpers.py

def generate_alert_html(region_name, region_id, timestamp, current, yesterday, last_week, history, reasons,a_threshold, b_threshold):
    """
    Genera cuerpo HTML del correo según datos de alerta
    """
    valid_history = [r for r in history if float(r.get("demHoy", 0)) > 0]

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h1 style="color:#D32F2F;">🚨 ¡Alerta CAMMESA!</h1>
        <p>Se ha detectado una caída significativa en la demanda eléctrica.</p>

        <hr style="margin: 20px 0;">

        <h2 style="color:#3F51B5;">📌 Configuración actual de alertas:</h2>
        <ul>
            <li><strong>A)</strong> Demanda actual es <strong>{a_threshold}%</strong> menor que la de Ayer y la Semana pasada (Se deben cumplir ambas)</li>
            <li><strong>B)</strong> Demanda actual es <strong>{b_threshold}%</strong> menor que la medición inmediata anterior</li>
        </ul>

        <h2 style="color:#3F51B5;">📍 Región: {region_name} (ID: {region_id})</h2>
        <p><strong>Hora:</strong> {timestamp}</p>

                <h2 style="color:#3F51B5;">📊 Valores registrados</h2>
        <table border="0" cellspacing="0" cellpadding="6" style="border-collapse: collapse; width: auto; margin: 0 auto; font-family: Arial, sans-serif;">
            <thead>
                <tr style="background-color: #FFEBEE; text-align: center;">
                    <th style="min-width: 120px; padding: 8px; border: 1px solid #ccc;">Medición</th>
                    <th style="min-width: 140px; padding: 8px; border: 1px solid #ccc;">Demanda (MW)</th>
                    <th style="min-width: 140px; padding: 8px; border: 1px solid #ccc;">Fecha / Hora</th>
                </tr>
            </thead>
"""

    # Mostrar datos por condición
    if any("menor que Ayer" in r for r in reasons):
        html += f"""
                <tr style="text-align: center;">
                    <td style="border: 1px solid #ccc; padding: 6px;">Hoy</td>
                    <td style="border: 1px solid #ccc; padding: 6px; color:red; font-weight:bold;">{current:.1f} MW</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{timestamp.split()[1]} hs</td>
                </tr>
                <tr style="text-align: center;">
                    <td style="border: 1px solid #ccc; padding: 6px;">Ayer</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{yesterday:.1f} MW</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{timestamp.split()[1]} hs</td>
                </tr>
                <tr style="text-align: center;">
                    <td style="border: 1px solid #ccc; padding: 6px;">Semana pasada</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{last_week:.1f} MW</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{timestamp.split()[1]} hs</td>
                </tr>
        """
    elif any("medición inmediata" in r for r in reasons) and len(valid_history) >= 2:
        record = valid_history[-2]
        prev_fecha = record.get("fecha").split("T")[1].split(".")[0] if record.get("fecha") else "N/A"
        prev_valor = float(record.get("demHoy", 0))

        html += f"""
                <tr style="text-align: center;">
                    <td style="border: 1px solid #ccc; padding: 6px;">Hoy</td>
                    <td style="border: 1px solid #ccc; padding: 6px; color:red; font-weight:bold;">{current:.1f} MW</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{timestamp.split()[1]} hs</td>
                </tr>
                <tr style="text-align: center;">
                    <td style="border: 1px solid #ccc; padding: 6px;">Medición anterior</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{prev_valor:.1f} MW</td>
                    <td style="border: 1px solid #ccc; padding: 6px;">{prev_fecha} hs</td>
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
    </body>
    </html>
    """

    return html
