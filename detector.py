# detector.py

def check_peak(current, yesterday, last_week, history, threshold_daily, threshold_last_measurement):
    """
    Devuelve (bool, list) → si hay alerta y causas
    Solo considera registros válidos (demHoy > 0)
    """
    reasons = []

    # Condición 1: Hoy < Ayer Y Semana pasada (ambos ≥25%)
    condition_1 = False
    if yesterday > 0 and last_week > 0:
        diff_yesterday = ((yesterday - current) / yesterday * 100)
        diff_last_week = ((last_week - current) / last_week * 100)

        if diff_yesterday >= threshold_daily and diff_last_week >= threshold_daily:
            reasons.append(f"Demanda actual ({current:.1f} MW) es {diff_yesterday:.1f}% menor que la de Ayer en el mismo horario({yesterday:.1f} MW)")
            reasons.append(f"Demanda actual ({current:.1f} MW) es {diff_last_week:.1f}% menor que la de la Semana pasada en el mismo horario ({last_week:.1f} MW)")
            condition_1 = True

    # Condición 2: Hoy < Medición inmediata anterior (≥20%)
    condition_2 = False
    previous_measurement = None

    # ✅ Filtrar solo registros válidos (demHoy > 0)
    valid_history = [r for r in history if float(r.get("demHoy", 0)) > 0]

    if len(valid_history) >= 2:
        # Última medición válida → valid_history[-1]
        # Penúltima medición válida → valid_history[-2]
        previous_record = valid_history[-2]
        previous_measurement = float(previous_record.get("demHoy", 0))

        if previous_measurement > 0:
            diff_previous = ((previous_measurement - current) / previous_measurement * 100)
            
            print("DEBUG - current:", current)
            print("DEBUG - previous_measurement:", previous_measurement)
            print("DEBUG - diff_previous:", diff_previous)

            if diff_previous >= threshold_last_measurement:
                reasons.append(
                    f"Demanda actual ({current:.1f} MW) es {diff_previous:.1f}% menor que la medición inmediata anterior ({previous_measurement:.1f} MW)"
                )
                condition_2 = True
        else:
            print("⚠️ No se pudo calcular la diferencia con la medición anterior")
    else:
        print("⚠️ No hay suficientes mediciones válidas para comparar")

    return condition_1 or condition_2, reasons
