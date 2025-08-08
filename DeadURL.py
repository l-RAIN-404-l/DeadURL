import subprocess
import os
import sys
print("Checking Packages...")
subprocess.run(["py", "-m", "playwright", "install"], check=True)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_console()
import pandas as pd
import asyncio
import shutil
import datetime

def backup_csv_file(csv_file):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(csv_file)
    if ext.lower() != ".csv":
        ext = ".csv"
    
    backup_path = f"{base}_backup_{timestamp}{ext}"
    shutil.copyfile(csv_file, backup_path)
    print(f"Backup created at: {backup_path}")
    return backup_path
if getattr(sys, 'frozen', False):
    base_path = pathlib.Path(sys._MEIPASS) / "ms-playwright"
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(base_path)
else:
    pass
from playwright.async_api import async_playwright
from tqdm import tqdm
import requests


CONCURRENT_LIMIT = 15
STEALTH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

results = {"🔴": []}
clean_csv_flag = False

def sanitize_url(url):
    url = url.strip().rstrip("/")
    if url.startswith("www."):
        url = "https://" + url
    return url if url.startswith("http") else None

async def check_url(browser, api_name, url, retry=False):
    try:
        context = await browser.new_context(extra_http_headers=STEALTH_HEADERS)
        page = await context.new_page()
        response = await page.goto(url, wait_until="domcontentloaded")
        status = response.status if response else "No Response"

        if status == 404:
            results["🔴"].append((url, status))
            tqdm.write(f"🔴 404 - {url} - [CTRL+CLICK] the link for manual check")

        await context.close()
        return status == 200

    except Exception as e:
        try:
            await context.close()
        except:
            pass
        return False

async def main():
    global clean_csv_flag

    print(":- Drop FilePath or File here :")
    csv_file = input("> ").strip().strip('\'"')

    if not os.path.exists(csv_file):
        print(":- File not found.")
        return
    
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f":- Error reading File: {e}")
        return

    print("")
    filter_domain = input(":- Scan a specific domain? (e.g. github.com)? [Leave blank to scan all]:\n> ").strip()

    clean_csv_input = input(":- Remove DEAD URLs from File after scan? (y/n): ").strip().lower()
    if clean_csv_input == 'y':
       print("")
       print("⚠️ - If you're on Windows, DISABLE 'Controlled Folder Access' in Windows Defender.")
       print("Otherwise, the script will fail to save the cleaned file.")
       print("You may re-enable it after")
       clean_csv_flag = True
       backup_csv_file(csv_file)
    else:
      print(":- Skipping cleaning.")
      clean_csv_flag = False

    url_list = []
    for i, row in df.iterrows():
        api = row.get("API_Name", f"Row{i}")
        for item in row.values:
            if isinstance(item, str):
                cleaned = sanitize_url(item)
                if cleaned and (filter_domain.lower() in cleaned.lower() if filter_domain else True):
                    url_list.append((api, cleaned))
    
    def clean_commas(file_path): 
     with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

     while ',,' in content:
        content = content.replace(',,', ',')

     with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    if not url_list:
        print("- No valid URLs found to scan.")
        return

    print(f"\n:- Ready to scan {len(url_list)} URLs...")
    input("- Press [ENTER] to launch scan.\n")

    async with async_playwright() as p:
     browser = await p.chromium.launch(headless=True)
     sem = asyncio.Semaphore(CONCURRENT_LIMIT)

     async def sem_check(api, url, pbar):
        async with sem:
            result = await check_url(browser, api, url)  # pass the single browser instance
            pbar.update(1)
            return result

     with tqdm(total=len(url_list), desc="Progress", dynamic_ncols=True) as pbar:
        tasks = [sem_check(api, url, pbar) for api, url in url_list]
        await asyncio.gather(*tasks)

    await browser.close()
    print("\n✅ Scan complete!")
    print(f"🔴 404 Errors: {len(results['🔴'])}")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    scan_result_file = f"scan_results_{timestamp}.txt"

    with open(scan_result_file, "w", encoding="utf-8") as f:
        f.write("🔴 404 Errors:\n")
        for url, status in results["🔴"]:
            f.write(f"{url} - {status}\n")

    print(f":- Report saved to {scan_result_file}") 

    if not clean_csv_flag:
        print(":- Cleanup skipped.")
        return

    print(":- Cleaning File...")
    bad_urls = set(url for url, _ in results["🔴"])
    cleaned_df = df.copy()

    for col in cleaned_df.columns:
        cleaned_df[col] = cleaned_df[col].apply(
            lambda x: None if isinstance(x, str) and sanitize_url(x) in bad_urls else x
        )

    cleaned_df.dropna(how='all', inplace=True)
    cleaned_df.to_csv(csv_file, index=False)
    clean_commas(csv_file)


    print(f":- File cleaned and saved.  {len(results['🔴'])} Dead URLs removed.")

import asyncio

if __name__ == "__main__":
    asyncio.run(main())
    