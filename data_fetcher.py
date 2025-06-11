# data_fetcher.py

import requests
from datetime import datetime

def parse_fecha(fecha_str):
    """Parsea fechas con o sin milisegundos o zona horaria"""
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        try:
            return datetime.strptime(fecha_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
        except ValueError as ve:
            print("❌ Error al parsear fecha:", ve)
            return None


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
            print(f"[Región {region_id}] ❌ Error en la solicitud HTTP: {response.status_code}")
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
                fecha_dt = parse_fecha(fecha_str)

                current = float(record.get("demHoy", 0) or record.get("Demanda", 0))
                yesterday = float(record.get("demAyer", 0) or record.get("DemandaAyer", 0))
                last_week = float(record.get("demSemanaAnt", 0) or record.get("DemandaSemanaAnterior", 0))

                if current <= 0 or yesterday <= 0 or last_week <= 0:
                    continue

                if fecha_dt and (latest_datetime is None or fecha_dt > latest_datetime):
                    latest_datetime = fecha_dt
                    latest_record = {
                        "current": current,
                        "yesterday": yesterday,
                        "last_week": last_week,
                        "timestamp": latest_datetime.strftime("%Y-%m-%d %H:%M:%S") if latest_datetime else None,
                        "history": data  # Lista completa para análisis posterior
                    }

        # Caso 2: La API devuelve un único dict
        elif isinstance(data, dict):
            fecha_str = data.get("fecha")
            fecha_dt = parse_fecha(fecha_str)

            current = float(data.get("demHoy", 0) or data.get("Demanda", 0))
            yesterday = float(data.get("demAyer", 0) or data.get("DemandaAyer", 0))
            last_week = float(data.get("demSemanaAnt", 0) or data.get("DemandaSemanaAnterior", 0))

            latest_record = {
                "current": current,
                "yesterday": yesterday,
                "last_week": last_week,
                "timestamp": fecha_dt.strftime("%Y-%m-%d %H:%M:%S") if fecha_dt else None,
                "history": [data]  # Guardamos el histórico como lista
            }

        if latest_record:
            return latest_record
        else:
            print(f"[Región {region_id}] ❌ No se encontró registro válido")
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
