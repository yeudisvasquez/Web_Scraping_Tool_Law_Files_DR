Web Scraping Tool – Law Files DR 🇩🇴

Python → Azure Data Lake (via AzCopy)

📌 Project Overview

This project automates the extraction of public procurement PDF documents from the Dominican Republic government procurement portal and stores them in Azure Data Lake Storage for downstream analytics, compliance, or archival use.

The solution follows a real-world data engineering pattern:

Web Scraping (Python) → Local Staging → Azure Data Lake (AzCopy)

🏗️ Architecture (Current Implementation)
Public Website (https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO)
      │
      ▼
Python Web Scraper (requests + BeautifulSoup / Playwright)
      │
      ▼
Local File System (raw PDFs)
      │
      ▼
AzCopy
      │
      ▼
Azure Data Lake Storage (Blob / ADLS Gen2)

🧰 Tech Stack
Python 3.10+
Playwright (for dynamic content & PDF downloads)
Requests / BeautifulSoup (HTML parsing)
AzCopy (high-performance upload to Azure Storage)
Azure Blob Storage / ADLS Gen2
Git & GitHub
VS Code

📁 Project Structure
Web_Scraping_Tool_Law_Files_DR/
│
├── src/
│   ├── pdf_ingestion.py      # Main scraping & download logic
│
├── data/
│   └── raw/
│       └── pdfs/             # Downloaded PDF files (local staging)
│
├── requirements.txt
├── README.md
└── .gitignore

⚙️ How It Works
1️⃣ Web Scraping (Python)
Navigates the procurement portal
Handles dynamic content where PDFs are only accessible after clicking Details
Downloads PDF contract files
Saves them locally under: data/raw/pdfs

2️⃣ Upload to Azure Data Lake (AzCopy)

Once files are downloaded locally, AzCopy is used to push them to Azure Storage.

Example command: azcopy copy "data/raw/pdfs" "https://<storage-account>.blob.core.windows.net/<container>/pdfs?<SAS_TOKEN>" --recursive

🔐 Authentication & Security
Azure authentication is handled using a SAS Token
No secrets are committed to GitHub
.gitignore excludes sensitive files and local data

🚀 This design mirrors how data engineering teams work in production:

Python handles custom extraction logic
Local disk is used as a staging layer
AzCopy provides fast, reliable bulk uploads
Azure Data Lake stores raw, immutable, unstructured data
Easy to later integrate with:
Azure Data Factory
Databricks
Synapse Analytics