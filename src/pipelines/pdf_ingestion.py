from playwright.sync_api import sync_playwright
import re
import os
from pathlib import Path
from dotenv import load_dotenv
import subprocess


def sanitize_folder_name(name: str) -> str:
    """
    Make a safe folder name for Windows / Linux / Azure
    """
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '_', name).strip()
    name = re.sub(r'\s+', '_', name)
    return name[:150]


def scrape_and_download():
    """Download files and organize them into per-notice folders"""

    load_dotenv()

    download_root = os.getenv("path_download_dir")
    if not download_root:
        raise ValueError("path_download_dir is not set in .env")

    Path(download_root).mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # -------------------------
        # STEP 1: Extract Notice UIDs
        # -------------------------
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(
            "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO",
            timeout=60000
        )

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        print("[*] Main page loaded")

        click_count = 0
        max_clicks = 1  # keep small for testing

        while click_count < max_clicks:
            more_items = page.locator(
                "a", has_text=re.compile(r"ver m[áa]s", re.IGNORECASE)
            )

            if more_items.count() > 0 and more_items.first.is_visible():
                click_count += 1
                print(f"[*] Clicking 'ver más' ({click_count}/{max_clicks})")
                more_items.first.scroll_into_view_if_needed()
                more_items.first.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)
            else:
                break

        notice_uids = []
        detalle_links = page.locator("a", has_text="DETALLE")
        total_links = detalle_links.count()

        print(f"[INFO] Found {total_links} DETALLE links")

        for i in range(total_links):
            onclick = detalle_links.nth(i).get_attribute("onclick")
            if onclick:
                match = re.search(r"'noticeUID='\s*\+\s*'([^']+)'", onclick)
                if match:
                    notice_uids.append(match.group(1).strip())

        browser.close()
        print(f"[INFO] Extracted {len(notice_uids)} notice UIDs")

        # ----------------------------------
        # STEP 2: Download files per notice
        # ----------------------------------
        base_url = "https://comunidad.comprasdominicana.gob.do"
        detail_endpoint = "/Public/Tendering/OpportunityDetail/Index"

        for idx, notice_uid in enumerate(notice_uids, 1):
            print(f"\n[{idx}/{len(notice_uids)}] Processing {notice_uid}")

            browser = p.chromium.launch(headless=True)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            detail_url = (
                f"{base_url}{detail_endpoint}"
                f"?noticeUID={notice_uid}&isModal=true&asPopupView=true"
            )

            page.goto(detail_url, timeout=60000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            # ----------------------------------
            # Extract notice title (folder name)
            # ----------------------------------
            try:
                # Target the 'Request Name:' label specifically and get the adjacent value
                # using following-sibling to pick up the name displayed on the website.
                req_name_locator = page.locator("xpath=//*[contains(text(), 'T[íi]tulo:')]").first
                if req_name_locator.count() > 0:
                    notice_title = req_name_locator.first.inner_text().strip()
                else:
                    # Fallback to header tags if specific label not found
                    notice_title = page.locator("h1, h2").first.inner_text().strip()
            except:
                notice_title = notice_uid

            folder_name = sanitize_folder_name(notice_title)
            notice_folder = Path(download_root) / folder_name
            notice_folder.mkdir(parents=True, exist_ok=True)

            print(f"    Folder: {notice_folder}")

            # ----------------------------------
            # Download files
            # ----------------------------------
            download_links = page.locator("a", has_text="Download")
            download_count = download_links.count()

            if download_count == 0:
                print("    [INFO] No files found")
                browser.close()
                continue

            print(f"    [FOUND] {download_count} file(s)")

            for i in range(download_count):
                try:
                    download_links = page.locator("a", has_text="Download")
                    link = download_links.nth(i)

                    with page.expect_download(timeout=60000) as d:
                        link.click()

                    download = d.value
                    filename = download.suggested_filename

                    file_path = notice_folder / filename
                    counter = 1

                    while file_path.exists():
                        stem = file_path.stem
                        suffix = file_path.suffix
                        file_path = notice_folder / f"{stem}_{counter}{suffix}"
                        counter += 1

                    download.save_as(file_path)
                    size_kb = file_path.stat().st_size / 1024

                    print(f"        [SAVED] {file_path.name} ({size_kb:.1f} KB)")

                except Exception as e:
                    print(f"        [ERROR] {str(e)[:80]}")

            browser.close()

        print("\n" + "=" * 70)
        print("[DONE] All downloads completed")
        print(f"Root download directory: {download_root}")
        print("=" * 70)


if __name__ == "__main__":
    scrape_and_download()