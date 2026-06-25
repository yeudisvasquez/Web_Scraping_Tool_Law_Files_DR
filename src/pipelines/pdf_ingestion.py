import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import re
import time

load_dotenv()

JSON_PATH = os.getenv("json_file_path") #folder where procesos.json is stored
if not JSON_PATH:
    raise ValueError("json_file_path is not set in .env")
DOWNLOAD_DIR = os.getenv("path_download_dir") #folder where PDF files will be downloaded
if not DOWNLOAD_DIR:
    raise ValueError("path_download_dir is not set in .env")

JSON_API_URL = os.getenv("DGCP_DOCUMENTS_URL") #API URL to fetch documents
if not JSON_API_URL:
    raise ValueError("DGCP_DOCUMENTS_URL is not set in .env")


def sanitize(name: str) -> str:
    """Sanitize folder name to remove invalid characters and limit length"""
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '_', name).strip()
    name = re.sub(r'\s+', '_', name)
    return name[:150]


def fetch_document_list(codigo_proceso: str):
    url = f"{JSON_API_URL}?proceso={codigo_proceso}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
    
        # API returns: { "payload": [ { "url": "...", "nombre": "...", ... } ] }
        return data["payload"]["content"]
    except Exception as e:
        print(f"    [WARN] Could not fetch documents for {codigo_proceso}: {str(e)[:80]}")
        return []


def download_files(url: str, folder: Path, filename: str):
    file_path = folder / filename

    for attempt in range(5):
        try:
            r = requests.get(url, stream=True, timeout=60)
            r.raise_for_status()

            with open(file_path, "wb") as f:
                for chunk in r.iter_content(8120):
                    f.write(chunk)

            print(f"    [SAVED] {filename}")
            return

        except Exception as e:
            wait = 2 ** attempt  # exponential backoff: 1,2,4,8,16
            print(f"    [RETRY {attempt+1}/5] Error: {str(e)[:80]} — waiting {wait}s")
            time.sleep(wait)

    print(f"    [FAILED] Could not download {filename}")

def main():
    procesos_file = Path(JSON_PATH) / "procesos.json"

    if not procesos_file.exists():
        raise FileNotFoundError(f"procesos.json not found at {procesos_file}")

    with open(procesos_file, "r", encoding="utf-8") as f:
        procesos = json.load(f)

    print(f"[*] Loaded {len(procesos)} procesos")

    for idx, p in enumerate(procesos, 1):
        codigo = p["codigo_proceso"]
        titulo = p["titulo"]

        print(f"\n[{idx}/{len(procesos)}] Processing {codigo}")
        
        # Create folder
        folder_name = sanitize(titulo)
        folder = Path(DOWNLOAD_DIR) / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        # Fetch document list
        docs = fetch_document_list(codigo) # API call

        time.sleep(1) # Limit API calls to 1 per second

        if not docs:
            print("    [INFO] No documents found")
            continue

        print(f"    [FOUND] {len(docs)} document(s)")

        # Download each document
        for doc in docs:
            file_url = doc["url_documento"]
            filename = sanitize(doc.get("nombre_documento", "document.pdf"))
            download_files(file_url, folder, filename)
            time.sleep(1.2) # Downloads up to 60 files per min

    print("\n[DONE] All documents downloaded.")

if __name__ == "__main__":
    main()