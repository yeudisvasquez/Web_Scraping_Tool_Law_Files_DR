import requests
from bs4 import BeautifulSoup
import os

def download_pdf(url, filename):
    print(f"Downloading: {filename}")

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed:", url)
        return

    os.makedirs("data/raw/pdfs", exist_ok=True)

    path = f"data/raw/pdfs/{filename}"

    with open(path, "wb") as f:
        f.write(response.content)

    print(f"Saved: {path}")


def scrape_pdfs():
    url = "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO"

    print("Requesting page...")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        print("Failed to load page")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    pdf_links = []

    print("Searching PDF links...")

    for link in links:
        href = link.get("href")

        if href and ".pdf" in href:
            pdf_links.append(href)

    print(f"Found {len(pdf_links)} PDF links")

    for i, pdf_url in enumerate(pdf_links[:5]):  # limit for testing

        if not pdf_url.startswith("http"):
            pdf_url = "https://comunidad.comprasdominicana.gob.do" + pdf_url

        download_pdf(pdf_url, f"file_{i}.pdf")


if __name__ == "__main__":
    scrape_pdfs()