from playwright.sync_api import sync_playwright
import json
# Diagnose how the website behaves when clicking on the "DETALLE" button. This is to understand if it opens a modal, navigates to a new page, or does something else, and to see if there are any download links available in that context.
def diagnose_detalle():
    """Diagnose what happens when clicking DETALLE"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(
            "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO",
            timeout=60000
        )

        page.wait_for_load_state("networkidle")
        print("[*] Page loaded.")
        page.wait_for_timeout(5000)

        # Get current URL
        print(f"\n[Current URL] {page.url}")
        
        # Find and click first DETALLE
        detalle = page.locator("text=DETALLE").first
        print(f"\n[DETALLE] Found, clicking...")
        
        detalle.click()
        print("[*] Clicked, waiting for modal...")
        page.wait_for_timeout(5000)

        # Check new URL
        print(f"\n[New URL] {page.url}")

        # Get page title
        print(f"[Title] {page.title()}")

        # Check for modal/dialog elements
        print("\n[MODAL] Checking for modal/dialog...")
        modals = page.locator("[role='dialog'], .modal, .popup, [class*='modal'], [class*='dialog']")
        print(f"  Found {modals.count()} modal elements")

        # Check for visible overlays
        overlays = page.locator("[class*='overlay'], [class*='backdrop'], [style*='display: block']")
        print(f"  Found {overlays.count()} overlay elements")

        # Get all visible text on page
        print("\n[TEXT] Page content:")
        visible_text = page.locator("body").inner_text()
        lines = [l.strip() for l in visible_text.split("\n") if l.strip() and len(l.strip()) > 2]
        for i, line in enumerate(lines):
            print(f"  {line[:120]}")

        # Check for links again
        print("\n[LINKS] All links on page:")
        all_links = page.locator("a")
        print(f"  Total links: {all_links.count()}")
        
        link_count = 0
        for i in range(all_links.count()):
            try:
                href = all_links.nth(i).get_attribute("href")
                text = all_links.nth(i).inner_text().strip()
                visible = all_links.nth(i).is_visible()
                if href and ('.zip' in href or '.pdf' in href or '.rar' in href or 'download' in href.lower()):
                    print(f"  [{i}] {text[:40]:40} -> {href[:80]} (visible: {visible})")
                    link_count += 1
            except:
                pass
        
        if link_count == 0:
            print("  No download links found")

        # Check for buttons
        print("\n[BUTTONS] All buttons on page:")
        buttons = page.locator("button")
        print(f"  Total buttons: {buttons.count()}")
        for i in range(min(20, buttons.count())):
            try:
                text = buttons.nth(i).inner_text().strip()
                if text and len(text) > 0:
                    print(f"  [{i}] {text[:50]}")
            except:
                pass

        # Try clicking on different DETALLE on the table
        print("\n[TRYING] Trying to find download in different ways...")
        
        # Look for specific elements that might contain download info
        procedure_download = page.locator("text=Descargar procedimiento, text=Download, text=Descargar")
        print(f"  'Descargar procedimiento' buttons: {procedure_download.count()}")

        browser.close()

if __name__ == "__main__":
    diagnose_detalle()
