import requests
from bs4 import BeautifulSoup

# Fetch one detail page to see the structure
notice_uid = "DO1.NTC.1728053"
url = f"https://comunidad.comprasdominicana.gob.do/Public/Tendering/OpportunityDetail/Index?noticeUID={notice_uid}&isModal=true&asPopupView=true"

session = requests.Session()
response = session.get(url, timeout=30)
response.encoding = 'utf-8'

print(f"[HTTP] Status: {response.status_code}")
print(f"[URL] {url}\n")

if response.status_code == 200:
    print("[HTML] First 2000 characters:")
    print(response.text[:2000])
    
    # Look for specific patterns
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
