DR Law Files Web Scraping Data Pipeline (Python + Azure)

- Azure Data Factory (Python Function Trigger)
- Python (Web Scraping)
- Azure Data Lake (Storage raw data)

Website to extract data from: https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index?currentLanguage=es-DO

Playwright (browser)
    ↓
PDF files
    ↓
Local storage (data/raw/pdfs)
    ↓
Azure Data Lake (pending)

## Data Pipeline

1. Scrape public Dominican Republic Licitaciones PDF files
2. Store locally under data/raw/pdfs
3. Upload raw files to Azure Data Lake Gen2
4. Raw zone ready for downstream processing