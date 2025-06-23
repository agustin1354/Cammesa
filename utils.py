# utils.py

def get_region_level(region_id, raw_data):
    """
    Devuelve el nivel de la región: 'PROVINCIA', 'REGION' o 'PAIS'
    """
    region_dict = {item["id"]: item for item in raw_data if "id" in item}

    if region_id == 1002:
        return "PAIS"

    region_info = region_dict.get(region_id, {})
    if region_info.get("idPadre") == 535052:
        return "REGION"
    elif region_info.get("idPadre") not in [None, 535052]:
        return "PROVINCIA"
    else:
        return "DESCONOCIDO"
