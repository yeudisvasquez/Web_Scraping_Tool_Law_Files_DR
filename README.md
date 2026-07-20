# Web Scraping Tool – Law Files DR 🇩🇴

**Automated extraction of public procurement PDFs from Dominican Republic government portal to Azure Data Lake Storage**

Python → Azure Data Lake (via AzCopy)

---

## 📌 Project Overview

This project automates the extraction of public procurement PDF documents from the Dominican Republic government procurement portal (Compras Dominicana) and stores them in Azure Data Lake Storage for downstream analytics, compliance, audit, and archival use.

The solution implements a production-ready data engineering pipeline that extracts contract notice documents, stages them locally, and uploads them to cloud storage for further processing and analytics.

### Key Features
- **Automated PDF Extraction**: Downloads contract notice documents from the procurement portal
- **Dynamic Content Handling**: Uses Playwright to handle JavaScript-rendered pages
- **Cloud Integration**: Uploads to Azure Data Lake Storage via AzCopy
- **Scheduled Processing**: Designed to work with Azure Data Factory for weekly automated runs
- **Duplicate Prevention**: Automatically removes local files after successful cloud upload
- **Security-First**: Uses SAS tokens and .gitignore for secret management

---

## 🏗️ Architecture & Workflow

```
Public Website (Compras Dominicana Portal)
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

Steps: 
      Downloads JSON file from API.
      Searches for URLs within the JSON files to download the documents in those URLs.
      Creates a folder on premises for each document and downloads it. 
      Copies all the documents to Azure Data Lake, programmed by Azure Data Factory to trigger the ETL process on a weekly basis. 
      Once the azcopy script is ran, the documents uploaded to the cloud are deleted from on premise to avoid duplicates.


##Project taking the following direction 
      
DGCP API
        │
        ▼
api_ingestion.py
        │
        ▼
Download JSON
        │
        ▼
Extract document URLs
        │
        ▼
Download PDFs
        │
        ▼
Azure Data Lake
(raw)
        │
        ▼
Azure Data Factory
        │
        ▼
Azure SQL Database
        │
        ▼
Power BI Dashboard