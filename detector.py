# detector.py

def check_peak(current, yesterday, last_week, history, threshold_daily=20, threshold_last_measurement=10):
    """
    Devuelve (bool, list) → si hay alerta y las razones
    """
    reasons = []

    # Condición 1: Hoy < Ayer Y Semana pasada (ambos ≥20%)
    condition_1 = False
    if yesterday > 0 and last_week > 0:
        diff_yesterday = ((yesterday - current) / yesterday * 100)
        diff_last_week = ((last_week - current) / last_week * 100)
        condition_1 = diff_yesterday >= threshold_daily and diff_last_week >= threshold_daily

        if diff_yesterday >= threshold_daily:
            reasons.append(f"Hoy ({current:.1f} MW) es {diff_yesterday:.1f}% menor que Ayer ({yesterday:.1f} MW)")
        if diff_last_week >= threshold_daily:
            reasons.append(f"Hoy ({current:.1f} MW) es {diff_last_week:.1f}% menor que Semana pasada ({last_week:.1f} MW)")

    # Condición 2: Hoy < Medición inmediata anterior (≥10%)
    condition_2 = False
    if len(history) >= 2:
        previous_record = history[1]  # Segundo registro más reciente
        previous_measurement = float(previous_record.get("demHoy", 0))

        if previous_measurement > 0:
            diff_previous = ((previous_measurement - current) / previous_measurement * 100)
            condition_2 = diff_previous >= threshold_last_measurement

            if condition_2:
                reasons.append(f"Hoy ({current:.1f} MW) es {diff_previous:.1f}% menor que la medición inmediata anterior ({previous_measurement:.1f} MW)")

    # Disparar alerta si cualquiera de las condiciones se cumple
    if condition_1 or condition_2:
        return True, reasons
    else:
        return False, reasons
