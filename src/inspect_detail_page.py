import requests # Library to make HTTP requests, to fetch the webpage content.
from bs4 import BeautifulSoup # Parse HTML content, read and search through.
# Script to load and inspect the structure of the website. 
# Inspect all links, buttons, and look for keywords related to downloading files.
# This is to explore the website to understand how is it built
# Fetch one detail page to see the structure
notice_uid = "DO1.NTC.1728053" # Unique identifier.
url = f"https://comunidad.comprasdominicana.gob.do/Public/Tendering/OpportunityDetail/Index?noticeUID={notice_uid}&isModal=true&asPopupView=true"
# Fetch the webpage content.
session = requests.Session() # Create a session to keep the connection open and make multiple requests.
response = session.get(url, timeout=30)
response.encoding = 'utf-8' # UTF-8 efor special characters.

print(f"[HTTP] Status: {response.status_code}")
print(f"[URL] {url}\n")

if response.status_code == 200: # Verify if page loaded successfully so then we can inspect it.
    print("[HTML] First 2000 characters:")
    print(response.text[:2000])
    
    # Look for specific patterns, link, buttons, and keywords.
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all links
    links = soup.find_all('a')
    print(f"\n[LINKS] Total: {len(links)}")
    for i, link in enumerate(links[:20]):
        href = link.get('href', '')
        text = link.get_text(strip=True)[:40]
        if href:
            print(f"  [{i}] {text:40} -> {href[:80]}")
    
    # Look for buttons
    buttons = soup.find_all('button')
    print(f"\n[BUTTONS] Total: {len(buttons)}")
    for i, btn in enumerate(buttons[:15]):
        text = btn.get_text(strip=True)
        onclick = btn.get('onclick', '')
        print(f"  [{i}] {text[:50]:50} onclick: {onclick[:60] if onclick else 'None'}")

    # Look for download keywords
    print(f"\n[KEYWORDS] Searching for download-related content...")
    if 'descargar' in response.text.lower():
        print("  Found: 'descargar'")
    if 'download' in response.text.lower():
        print("  Found: 'download'")
    if '.zip' in response.text:
        print("  Found: '.zip'")
    if '.pdf' in response.text:
        print("  Found: '.pdf'")
