from playwright.sync_api import sync_playwright # playwright to see exactly what humans see. JavaScript friendly.
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    # Page navigation and interaction.
    page.goto(
        "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO",
        timeout=60000
    )

    page.wait_for_load_state("networkidle") #Wait for the page to load completely, including JavaScript.
    page.wait_for_timeout(3000) 

    detalle_links = page.locator("a", has_text="DETALLE") # Location of the element containing the "onclick" attribute with the noticeUID.
    
    if detalle_links.count() > 0:
        link = detalle_links.first
        onclick = link.get_attribute("onclick")
        
        print("[ONCLICK ATTRIBUTE]")
        print(onclick[:500])
        print("\n[SEARCHING FOR noticeUID]")
        
        # Try different patterns/ Iterate through different patterns to find the noticeUID in the onclick attribute.
        # Debugging: Print the matches for each pattern to see which one works best.
        patterns = [
            r"'noticeUID='\s*\+\s*'([^']+)'", #Matches: 'noticeUID=' + 'DO1.NTC.1728053'
            r"noticeUID=.*?'([^']+)'",
            r"noticeUID='([^']+)'",
            r"\+'([A-Z0-9.]+)'\+",
        ]
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, onclick)
            print(f"\nPattern {i}: {pattern}")
            print(f"  Matches: {matches}")

    browser.close()
