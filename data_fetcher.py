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
        "timestamp": fecha_hora_del_registro
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
                "timestamp": None
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
                    except ValueError as ve:
                        print(f"[Región {region_id}] ❌ Error al parsear fecha:", ve)
                        continue

                current = (
                    record.get("Demanda") or
                    record.get("demHoy") or
                    record.get("valor") or
                    record.get("demand", None)
                )

                if current is not None:
                    if latest_datetime is None or fecha_dt > latest_datetime:
                        latest_datetime = fecha_dt
                        latest_record = record

        # Caso 2: La API devuelve un único dict
        elif isinstance(data, dict):
            latest_record = data
            fecha_str = data.get("fecha")
            if fecha_str:
                try:
                    latest_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                except ValueError:
                    latest_datetime = datetime.strptime(fecha_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")

        if latest_record:
            current = (
                latest_record.get("Demanda") or
                latest_record.get("demHoy") or
                latest_record.get("valor") or
                None
            )
            yesterday = (
                latest_record.get("DemandaAyer") or
                latest_record.get("demAyer") or
                latest_record.get("valorAyer") or
                None
            )
            last_week = (
                latest_record.get("DemandaSemanaAnterior") or
                latest_record.get("demSemanaAnt") or
                latest_record.get("valorSemanaAnterior") or
                None
            )

            if current is None:
                print(f"[Región {region_id}] ❌ No se encontró valor de 'Demanda'")
            if yesterday is None:
                print(f"[Región {region_id}] ❌ No se encontró valor de 'DemandaAyer'")
            if last_week is None:
                print(f"[Región {region_id}] ❌ No se encontró valor de 'DemandaSemanaAnterior'")

            if current is not None and yesterday is not None and last_week is not None:
                return {
                    "current": float(current),
                    "yesterday": float(yesterday),
                    "last_week": float(last_week),
                    "timestamp": latest_datetime.strftime("%Y-%m-%d %H:%M:%S") if latest_datetime else None
                }

        print(f"[Región {region_id}] ❌ No se encontraron datos válidos")
        return {
            "current": None,
            "yesterday": None,
            "last_week": None,
            "timestamp": None
        }

    except Exception as e:
        print(f"[Región {region_id}] ❌ Error al obtener datos:", e)
        return {
            "current": None,
            "yesterday": None,
            "last_week": None,
            "timestamp": None
        }