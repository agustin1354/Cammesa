# helpers.py

def generate_alert_html(region_name, region_id, timestamp, current, yesterday, last_week, history, reasons):
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
            <li><strong>A)</strong> Demanda actual es <strong>{reasons.A_THRESHOLD}%</strong> menor que la de Ayer y la Semana pasada (Se deben cumplir ambas)</li>
            <li><strong>B)</strong> Demanda actual es ≥<strong>{reasons.B_THRESHOLD}%</strong> menor que la medición inmediata anterior</li>
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

    # Mostrar datos por condición
    if any("menor que Ayer" in r for r in reasons):
        fecha_ayer = "última medición"
        fecha_semana = "última medición"

        html += f"""
            <tr>
                <td>Hoy</td>
                <td style="text-align:right; color:red; font-weight:bold;">{current:.1f} MW</td>
                <td style="text-align:center;">{timestamp.split()[1]} hs</td>
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

    elif any("medición inmediata" in r for r in reasons):
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
    </body>
    </html>
    """

    return html
