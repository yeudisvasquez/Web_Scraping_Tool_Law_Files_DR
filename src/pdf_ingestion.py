from playwright.sync_api import sync_playwright
import re
import os
import time

def scrape_and_download():
    """Download all zip files from Contract Notice Management website"""
    
    with sync_playwright() as p:
        # Extract Notice UIDs from the main page
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Path to download directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(base_path, "data", "raw")
        os.makedirs(download_dir, exist_ok=True)

        page.goto(
            "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO",
            timeout=60000
        )

        page.wait_for_load_state("networkidle")
        print("[*] Page loaded...")
        page.wait_for_timeout(3000)

        # Click "more items" until no longer visible or limit reached for testing
        # Click "more items" until no longer visible to ensure all records are loaded
        # while True:
        click_count = 0
        max_clicks = 10
        while click_count < max_clicks:
            # Use regex to handle case sensitivity and the accent in "más"
            more_items_link = page.locator("a", has_text=re.compile(r"ver m[áa]s", re.IGNORECASE))
            
            if more_items_link.count() > 0 and more_items_link.first.is_visible():
                click_count += 1
                # print("    - Clicking 'more items' link...")
                print(f"    - Clicking 'more items' link ({click_count}/{max_clicks})...")
                more_items_link.first.scroll_into_view_if_needed()
                more_items_link.first.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)  # Wait for content to render
            else:
                break

        print("[*] All items loaded. Extracting notice UIDs...")

        # Extract all noticeUIDs from DETALLE links
        notice_uids = []
        
        detalle_links = page.locator("a", has_text="DETALLE")
        total_links = detalle_links.count()
        print(f"[INFO] Found {total_links} DETALLE links")

        for i in range(total_links):
            try:
                link = detalle_links.nth(i)
                onclick = link.get_attribute("onclick")
                
                if onclick:
                    # Extract noticeUID from onclick attribute
                    # Pattern: 'noticeUID=' + 'DO1.NTC.1728053'
                    match = re.search(r"'noticeUID='\s*\+\s*'([^']+)'", onclick)
                    
                    if match:
                        notice_uid = match.group(1).strip()
                        notice_uids.append(notice_uid)
                        print(f"  [{i+1}] {notice_uid}")
            except Exception as e:
                print(f"  [ERROR] Extracting UID {i}: {str(e)}")
                continue

        browser.close()

        print(f"\n[EXTRACTED] {len(notice_uids)} notice UIDs")

        # Now download files for each notice
        downloaded_files = []
        base_url = "https://comunidad.comprasdominicana.gob.do"
        detail_endpoint = "/Public/Tendering/OpportunityDetail/Index"
        
        for idx, notice_uid in enumerate(notice_uids, 1):
            try:
                print(f"\n[{idx}/{len(notice_uids)}] Processing {notice_uid}...")
                
                # Create a new browser context for download handling
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(accept_downloads=True)
                page = context.new_page()
                
                # Navigate to detail page
                detail_url = f"{base_url}{detail_endpoint}?noticeUID={notice_uid}&isModal=true&asPopupView=true"
                page.goto(detail_url, timeout=60000)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)
                
                # Find all Download links
                download_links = page.locator("a", has_text="Download")
                download_count = download_links.count()
                
                if download_count == 0:
                    print(f"      [INFO] No download links found")
                    browser.close()
                    continue
                
                print(f"      [FOUND] {download_count} download link(s)")
                
                # Click each download link
                for link_idx in range(download_count):
                    try:
                        # Re-query in case DOM changed
                        download_links = page.locator("a", has_text="Download")
                        if link_idx >= download_links.count():
                            break
                        
                        link = download_links.nth(link_idx)
                        link_text = link.inner_text()
                        
                        print(f"        [DOWNLOAD {link_idx+1}] {link_text[:50]}")
                        
                        # Trigger download
                        with page.expect_download(timeout=60000) as download_info:
                            link.click()
                        
                        download = download_info.value
                        filename = download.suggested_filename
                        
                        # Avoid duplicates
                        file_path = os.path.join(download_dir, filename)
                        counter = 1
                        base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
                        ext = '.' + filename.rsplit('.', 1)[1] if '.' in filename else ''
                        
                        while os.path.exists(file_path):
                            file_path = os.path.join(download_dir, f"{base_name}_{counter}{ext}")
                            counter += 1
                        
                        download.save_as(file_path)
                        file_size = os.path.getsize(file_path) / 1024  # KB
                        print(f"        [SAVED] {os.path.basename(file_path)} ({file_size:.1f} KB)")
                        downloaded_files.append(file_path)
                        
                    except Exception as e:
                        print(f"        [ERROR] Download {link_idx}: {str(e)[:80]}")
                        continue
                
                browser.close()
                
            except Exception as e:
                print(f"      [ERROR] Processing notice: {str(e)[:100]}")
                try:
                    browser.close()
                except:
                    pass
                continue

        # Print summary
        print("\n" + "="*70)
        print(f"[SUMMARY] Download Complete")
        print("="*70)
        print(f"Processed: {len(notice_uids)} items")
        print(f"Downloaded: {len(downloaded_files)} files")
        
        if downloaded_files:
            print("\nFiles saved:")
            for file in downloaded_files:
                filename = os.path.basename(file)
                size = os.path.getsize(file) / 1024  # KB
                print(f"  [OK] {filename} ({size:.1f} KB)")
        else:
            print("[INFO] No files were downloaded")
        
        print("="*70)
        print(f"\nDownload directory: {download_dir}")

if __name__ == "__main__":
    scrape_and_download()