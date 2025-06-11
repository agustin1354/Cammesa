# detector.py


def check_peak(current, yesterday, last_week, history, threshold_daily=20, threshold_last_measurement=10):
    

    """
    Devuelve (bool, list) → si hay alerta y causas
    """
    reasons = []

    # Condición 1: Hoy < Ayer Y Semana pasada (ambos ≥20%)
    condition_1 = False
    diff_yesterday = ((yesterday - current) / yesterday * 100) if yesterday > 0 else 0
    diff_last_week = ((last_week - current) / last_week * 100) if last_week > 0 else 0

    if diff_yesterday >= threshold_daily and diff_last_week >= threshold_daily:
        reasons.append(f"Hoy ({current:.1f} MW) es {diff_yesterday:.1f}% menor que Ayer ({yesterday:.1f} MW)")
        reasons.append(f"Hoy ({current:.1f} MW) es {diff_last_week:.1f}% menor que Semana pasada ({last_week:.1f} MW)")
        condition_1 = True

    # Condición 2: Hoy < Medición inmediata anterior (≥10%)
    condition_2 = False
    previous_measurement = None

    if len(history) >= 2:
        record = history[1]
        previous_measurement = float(record.get("demHoy", 0))
        
        print("DEBUG - current:", current)
        print("DEBUG - previous_measurement:", previous_measurement)
        print("DEBUG - diff_previous:", diff_previous)

        if previous_measurement > 0:
            diff_previous = ((previous_measurement - current) / previous_measurement * 100)
            if diff_previous >= threshold_last_measurement:
                reasons.append(f"Hoy ({current:.1f} MW) es {diff_previous:.1f}% menor que la medición inmediata anterior ({previous_measurement:.1f} MW)")
                condition_2 = True

    return condition_1 or condition_2, reasons
