import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("DGCP_API_URL")
OUTPUT_JSON_PATH = os.getenv("json_file_path")

#Fields to extract from the API response
FIELDS = [
    "codigo_proceso",
    "unidad_compra",
    "titulo",
    "estado_proceso",
    "divisa",
    "monto_estimado",
    "url",
    "duracion_contrato"
]

def fetch_all_procesos():
    page = 0
    all_items = []

    while True:
        url = f"{API_URL}?page={page}&size=100"
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        items = data["payload"]["content"]
        all_items.extend(items)

        total_pages = data["payload"]["totalPages"]
        if page >= total_pages - 1:
            break

        page += 1

    return all_items

def extract_fields(proceso):
    "Return only the fields specified in FIELDS"
    return {field: proceso.get(field) for field in FIELDS}

def main():
    print("[*] Fetching data from API...")
    procesos = fetch_all_procesos()

    print(f"[*] Total procesos fetched: {len(procesos)}")

    filtered_procesos = [extract_fields(proceso) for p in procesos]

    #Save to JSON file
    with open(os.path.join(OUTPUT_JSON_PATH, "procesos.json"), "w", encoding="utf-8") as f:
        json.dump(filtered_procesos, f, ensure_ascii=False, indent=4)

    print(f"[*] Data saved to {os.path.join(OUTPUT_JSON_PATH, 'procesos.json')}")

if __name__ == "__main__":
    main()