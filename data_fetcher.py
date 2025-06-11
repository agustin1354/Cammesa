# data_fetcher.py

import requests
from datetime import datetime


def get_demand_comparison_values(region_id):
    """
    Devuelve:
    {
        "current": demHoy,
        "yesterday": demAyer,
        "last_week": demSemanaAnt,
        "timestamp": fecha_hora_del_registro,
        "history": [lista_completa_de_datos]
    }
    """
    API_URL = f"https://api.cammesa.com/demanda-svc/demanda/ObtieneDemandaYTemperaturaRegion?id_region={region_id}"

    try:
        response = requests.get(API_URL)

        if response.status_code != 200:
            print(f"[Región {region_id}] ❌ Error en la solicitud HTTP")
            return {
                "current": None,
                "yesterday": None,
                "last_week": None,
                "timestamp": None,
                "history": []
            }

        data = response.json()
        latest_record = None
        latest_datetime = None

        # Caso 1: La API devuelve una lista de registros 
        if isinstance(data, list):
            for record in data:
                fecha_str = record.get("fecha")
                if not fecha_str:
                    continue
                try:
                    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                except ValueError:
                    try:
                        fecha_dt = datetime.strptime(fecha_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    except Exception as ve:
                        print(f"[Región {region_id}] ❌ Error al parsear fecha:", ve)
                        continue

                current = (
                    record.get("Demanda") or
                    record.get("demHoy") or
                    record.get("valor") or
                    None
                )
                yesterday = (
                    record.get("DemandaAyer") or
                    record.get("demAyer") or
                    record.get("valorAyer") or
                    None
                )
                last_week = (
                    record.get("DemandaSemanaAnterior") or
                    record.get("demSemanaAnt") or
                    record.get("valorSemanaAnterior") or
                    None
                )

                if current is not None and yesterday is not None and last_week is not None:
                    latest_record = record
                    latest_datetime = fecha_dt
                    break

        elif isinstance(data, dict):
            latest_record = data
            fecha_str = data.get("fecha")
            if fecha_str:
                try:
                    latest_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                except ValueError:
                    latest_datetime = datetime.strptime(fecha_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")

        if latest_record:
            current = float(latest_record.get("Demanda", 0) or latest_record.get("demHoy", 0) or latest_record.get("valor", 0))
            yesterday = float(latest_record.get("DemandaAyer", 0) or latest_record.get("demAyer", 0) or latest_record.get("valorAyer", 0))
            last_week = float(latest_record.get("DemandaSemanaAnterior", 0) or latest_record.get("demSemanaAnt", 0) or latest_record.get("valorSemanaAnterior", 0))

            # Obtener historial completo para comparar con medición inmediata anterior
            history = data if isinstance(data, list) else []

            return {
                "current": current,
                "ayer": yesterday,
                "semana_anterior": last_week,
                "timestamp": latest_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "history": history
            }

        else:
            print(f"[Región {region_id}] ❌ No se encontró un registro válido")
            return {
                "current": None,
                "yesterday": None,
                "last_week": None,
                "timestamp": None,
                "history": []
            }

    except Exception as e:
        print(f"[Región {region_id}] ❌ Error al obtener datos:", e)
        return {
            "current": None,
            "yesterday": None,
            "last_week": None,
            "timestamp": None,
            "history": []
        }
