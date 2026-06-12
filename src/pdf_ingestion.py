import requests
from bs4 import BeautifulSoup

def scrape_example():
    url = "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO"

    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text

    data = {
        "title": title,
        "url": url
    }

    print(data)

if __name__ == "__main__":
    scrape_example()