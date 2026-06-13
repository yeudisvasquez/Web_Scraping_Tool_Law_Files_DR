#requests and BeautifulSoup libraries are used to send HTTP requests and parse HTML content, respectively. The os library is used to create directories and manage file paths.
#Send HHTP request to the website and parse the HTML content to extract PDF links, then download the PDFs and save them to a specified directory.
import requests
from bs4 import BeautifulSoup
import os

#Function to scrape the website and download PDFs
def scrape_example():
    url = "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO"
    #Send Get request to the URL and store the response in the variable respone
    response = requests.get(url)

    #Check if the request was successful (status code 200) if not, print and exit the function
    if response.status_code != 200:
        print("Failes to fetch data")
        return

    #Parse the HTML content of the response using BeautifulSoup and store it in the variable soup
    soup = BeautifulSoup(response.content, 'html.parser')

    #extract the page title and stor it in the variable
    title = soup.title.string.text

    #Data dictionary (Python dictionary with 2 keys: "title" and "url") to store the title of the page and the URL of the page. The values for these keys are obtained from the title variable and the url variable, respectively.
    data = {
        "title": title,
        "url": url
    }
    #print result to the terminal
    print(data)
#Run the function when the script is executed (Check if the script is being run directly, not imported as a module)
if __name__ == "__main__":
    scrape_example()