# detector.py

def check_peak(current, yesterday, last_week, threshold_percentage=20):
   if None in (current, yesterday, last_week):
        print("❌ No se pueden calcular picos: uno o más valores son None")
        return False, []

    # Calcular porcentajes de caída
    diff_yesterday = ((yesterday - current) / yesterday) * 100
    diff_last_week = ((last_week - current) / last_week) * 100

    reasons = []

    below_yesterday = diff_yesterday >= threshold_percentage
    below_last_week = diff_last_week >= threshold_percentage

    if below_yesterday:
        reasons.append(f"Hoy ({current:.1f} MW) es {diff_yesterday:.1f}% menor que Ayer ({yesterday:.1f} MW)")

    if below_last_week:
        reasons.append(f"Hoy ({current:.1f} MW) es {diff_last_week:.1f}% menor que Semana Pasada ({last_week:.1f} MW)")

    # Alerta solo si ambas condiciones se cumplen
    if below_yesterday and below_last_week:
        return True, reasons
    else:
        return False, reasons
