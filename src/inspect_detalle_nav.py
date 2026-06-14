from playwright.sync_api import sync_playwright
import json

def inspect_detalle_navigation():
    """Check if DETALLE navigates to a new page"""
    
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

        print(f"[URL Before] {page.url}")
        
        # Find DETALLE buttons and check their attributes.
        detalle_links = page.locator("a, button", has_text="DETALLE")
        print(f"[Found] {detalle_links.count()} DETALLE links/buttons")
        
        if detalle_links.count() > 0:
            first_detalle = detalle_links.first
            
            # Check if it's a link (a tag) or button
            tag_name = first_detalle.evaluate("el => el.tagName")
            print(f"[Tag] {tag_name}")
            
            # Get the onclick attribute if it exists
            onclick = first_detalle.get_attribute("onclick")
            href = first_detalle.get_attribute("href")
            data_attrs = first_detalle.evaluate("""
                el => {
                    const attrs = {};
                    for (let i = 0; i < el.attributes.length; i++) {
                        attrs[el.attributes[i].name] = el.attributes[i].value;
                    }
                    return attrs;
                }
            """)
            
            print(f"[Href] {href}")
            print(f"[OnClick] {onclick}")
            print(f"[All Attributes]:")
            for key, val in data_attrs.items():
                if key not in ['class', 'style']:
                    print(f"  {key}: {val}")
            
            # Try to find the parent row and get the link it contains
            row_parent = first_detalle.locator("..")
            row_links = row_parent.locator("a[href]")
            print(f"\n[Row Links] Found {row_links.count()} links in the same row:")
            for i in range(min(5, row_links.count())):
                try:
                    link_href = row_links.nth(i).get_attribute("href")
                    link_text = row_links.nth(i).inner_text()
                    if link_href and "javascript" not in link_href:
                        print(f"  [{i}] {link_text[:40]:40} -> {link_href[:100]}")
                except:
                    pass

            # Check what's in the row table cells
            cells = row_parent.locator("td")
            print(f"\n[Row Content] {cells.count()} cells")
            for i in range(min(7, cells.count())):
                try:
                    cell_text = cells.nth(i).inner_text()[:60]
                    print(f"  Cell {i}: {cell_text}")
                except:
                    pass

        browser.close()

if __name__ == "__main__":
    inspect_detalle_navigation()
