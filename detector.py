# detector.py

def check_peak(current, yesterday, last_week, previous_measurement, threshold_daily=20, threshold_last_measurement=10):
    """
    Devuelve (bool, list) → si hay alerta y las razones
    """
    reasons = []

    # Condición 1: Hoy es 20% menor que Ayer Y que Semana pasada
    diff_yesterday = ((yesterday - current) / yesterday * 100) if yesterday > 0 else 0
    diff_last_week = ((last_week - current) / last_week * 100) if last_week > 0 else 0

    condition_1 = diff_yesterday >= threshold_daily and diff_last_week >= threshold_daily

    if condition_1:
        reasons.append(f"Hoy ({current:.0f} MW) es {diff_yesterday:.1f}% menor que Ayer ({yesterday:.0f} MW)")
        reasons.append(f"Hoy ({current:.0f} MW) es {diff_last_week:.1f}% menor que Semana pasada ({last_week:.0f} MW)")

    # Condición 2: Hoy es 10% menor que la medición inmediata anterior
    diff_previous = ((previous_measurement - current) / previous_measurement * 100) if previous_measurement > 0 else 0
    condition_2 = diff_previous >= threshold_last_measurement

    if condition_2:
        reasons.append(f"Hoy ({current:.0f} MW) es {diff_previous:.1f}% menor que la medición anterior ({previous_measurement:.0f} MW)")

    # Disparar alerta si se cumple cualquiera de las condiciones
    if condition_1 or condition_2:
        return True, reasons
    else:
        return False, reasons
