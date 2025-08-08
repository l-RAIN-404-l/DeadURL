First project i made for fun lol :D

# 🔥URL Scanner

A super-efficient, async URL scanner that checks thousands of URLs from a file (.csv/.txt) for dead links (404s)
This program can be use to clean a large list of URLs from broken ones.

---

## ⚡ Features

- **Async scanning** with concurrency limit (default 15) for fast performance  
- **Domain filtering** — scan all URLs or can target specific domains only from the file 
- **CSV cleaning** — automatically remove dead URLs from your CSV (Optional) [BETA]
- **Backup system** — backs up your original CSV before cleaning  
- **Scan-Result Produces** — shows all dead Urls found
- **Supports most Url's format** — http://, https://, www.
- **Stealth headers** — mimics real browser requests for better detection bypassing most Web-security-bots 
- **Progress bar** — live scan progress displayed with tqdm  
- **Platform** — works on Windows, Linux  (Not tested on MacOS)
- **Optimized for low hardware** — 

---

## ⚠️ Important Windows Users Notice

Please note if you do not want to clean your file from dead urls and only want a scan and a ScanResult report, you may skip this step  :

If you are running this on **Windows**, **disable** the **"Controlled Folder Access"** feature in **Windows Defender** **before running the cleaning step**.

Steps:
   1. Open Windows Security
   2. Go to virus & threat protection
   3. Click Manage ransomware protection
   4. Turn off Controlled Folder Access
You may re-enable this after the scan is completed

---

## 🚀 How to Use

1. Clone or download this repo  
2. Run `pip install -r requirements.txt` 
   OR  `py -m pip install -r requirements.txt` 
   OR  `python -m pip install -r requirements.txt` to install dependencies  
3. Start the scanner :

    ```bash
    py DeadURL.py
    ```
    or
     ```bash
    python DeadURL.py
    ```

4. When prompted:  
    - **Drop or enter the full path** to your CSV file  
    - **Optionally scan a specified domain** (or leave blank to scan all)  
    - **Choose whether to remove dead URLs** from the CSV after scan (y/n)  
5. Wait for the scan to complete  
6. Check the generated `scan_results_YYYY-MM-DD_HH-MM-SS.txt` file for 404 errors  
7. If cleaning was enabled, your original CSV will be backed up and cleaned of dead URLs  

---

## 💻 Code Overview & Customization

- **Concurrency limit** can be adjusted by changing `CONCURRENT_LIMIT` at the top of the script for faster/slower scanning depending on your hardware/network  
- The **User-Agent and headers** are set in `STEALTH_HEADERS` — you can update to mimic different browsers or add custom headers if needed  
- The script uses [Playwright](https://playwright.dev/python/) to simulate browser requests for better accuracy over simple HTTP requests   
- URLs are sanitized to only accept those starting with `http`, `https`, or `www.` — can be tweaked inside `sanitize_url()`  
- File cleaning will remove only the dead URLs and save a backup automatically  

---

## 📁 File Format

- The file should contain URLs, ideally with a column named `API_Name` (optional)  
- URLs can start with `http://`, `https://`, or `www.`  
- URLs can be separated by commas, spaces, or new lines inside cells  

---

## 🛠️ Requirements

- Python 3.7+  
- Playwright  
- pandas  
- tqdm  
- requests  

---

## 📜 License



---

## 🤝 Contributions

Pull requests and issues are welcome! 
This project is still under development so issues may arise :(