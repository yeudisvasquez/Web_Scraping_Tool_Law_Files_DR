import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("DGCP_API_URL")
OUTPUT_JSON_PATH = os.getenv("json_file_path")

if not API_URL:
    raise ValueError("DGCP_API_URL is missing in .env")

if not OUTPUT_JSON_PATH:
    raise ValueError("json_file_path is missing in .env")

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

    #while True:
    for page in range(0, 50):  # Limit to 50 pages for testing
        url = f"{API_URL}?page={page}&limit=1000"
        print(f"[*] Fetching page {page}...")

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        items = data["payload"]["content"]

        if not items:
            print("[*] No more pages. Finished.")
            break

        all_items.extend(items)
        page += 1

    return all_items

def extract_fields(proceso):
    "Return only the fields specified in FIELDS"
    return {field: proceso.get(field) for field in FIELDS}

def main():
    print("[*] Fetching data from API...")
    procesos = fetch_all_procesos()

    print(f"[*] Total procesos fetched: {len(procesos)}")

    filtered_procesos = [extract_fields(p) for p in procesos]

    #Save to JSON file
    with open(os.path.join(OUTPUT_JSON_PATH, "procesos.json"), "w", encoding="utf-8") as f:
        json.dump(filtered_procesos, f, ensure_ascii=False, indent=4)

    print(f"[*] Data saved to {os.path.join(OUTPUT_JSON_PATH, 'procesos.json')}")

if __name__ == "__main__":
    main()