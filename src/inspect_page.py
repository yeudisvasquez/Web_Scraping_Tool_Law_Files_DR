from playwright.sync_api import sync_playwright
import json

def inspect_page():
    """Inspect the page structure to understand how to interact with it"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(
            "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO",
            timeout=60000
        )

        page.wait_for_load_state("networkidle")
        print("🔎 Page loaded. Inspecting structure...\n")

        # Wait for content to render
        page.wait_for_timeout(5000)

        # Get page title
        title = page.title()
        print(f"📄 Page Title: {title}\n")

        # Find all buttons
        buttons = page.locator("button")
        print(f"📌 Total BUTTON elements: {buttons.count()}")
        
        if buttons.count() > 0:
            print("\n🔘 First 20 button texts:")
            for i in range(min(20, buttons.count())):
                try:
                    text = buttons.nth(i).inner_text().strip()
                    if text:
                        print(f"   {i}: {text}")
                except:
                    pass

        # Find links
        links = page.locator("a")
        print(f"\n🔗 Total LINK elements: {links.count()}")
        
        if links.count() > 0:
            print("   First 15 links with href:")
            for i in range(min(15, links.count())):
                try:
                    href = links.nth(i).get_attribute("href")
                    text = links.nth(i).inner_text().strip()
                    if href:
                        print(f"   {i}: {text[:50]} -> {href[:80]}")
                except:
                    pass

        # Find tables
        tables = page.locator("table")
        print(f"\n📊 Total TABLE elements: {tables.count()}")

        # Find divs with specific classes that might contain data
        print("\n📦 Looking for data containers:")
        
        # Check for common table/data structures
        rows = page.locator("tr")
        print(f"   Total TR (table rows): {rows.count()}")
        
        divs = page.locator("div[role='row']")
        print(f"   Total divs with role='row': {divs.count()}")

        # Get all text on the page
        page_text = page.inner_text("body")
        lines = page_text.split("\n")
        print("\n📝 Page content (first 30 non-empty lines):")
        non_empty_lines = [l.strip() for l in lines if l.strip() and len(l.strip()) > 3]
        for i, line in enumerate(non_empty_lines[:30]):
            print(f"   {line[:100]}")

        # Look for DETALLE text specifically
        print("\n🔍 Searching for 'DETALLE' text:")
        detalle_elements = page.locator("text=/DETALLE/i")
        print(f"   Found {detalle_elements.count()} elements containing 'DETALLE'")
        
        # Look for download links
        print("\n⬇️ Searching for download links (.zip, .pdf, etc.):")
        zip_links = page.locator("a[href*='.zip']")
        print(f"   Found {zip_links.count()} .zip links")
        
        pdf_links = page.locator("a[href*='.pdf']")
        print(f"   Found {pdf_links.count()} .pdf links")

        # Get page HTML structure (condensed)
        print("\n🏗️ HTML Structure sample:")
        html = page.content()
        # Find the main content area
        if '<body' in html:
            body_start = html.find('<body')
            body_sample = html[body_start:body_start+2000]
            print(body_sample[:500])

        browser.close()

if __name__ == "__main__":
    inspect_page()
