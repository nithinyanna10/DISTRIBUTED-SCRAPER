# 🕸️ Distributed Web Scraper with Streamlit GUI + NLP Intelligence

This project is a powerful, extensible web scraping system that allows users to:

- Search and scrape content from the web (titles, headers, links, or full text)
- Run scraping tasks in parallel using multiprocessing
- Analyze and visualize the results using NLP techniques like summarization and keyword extraction
- Export data as CSV/JSON
- Interact with it via a beautiful Streamlit GUI

---

## 🚀 Features

### 🔍 Web Scraping
- Search the web using DuckDuckGo Search API
- Scrape data from N top-ranked websites
- Choose what to scrape: titles, headers, links, or paragraph text
- Filter content based on word count
- Automatic retries, logging, and duplicate URL removal

### ⚙️ Architecture
- **Multiprocessing-based scraping** for speed and parallelism
- Modular design (`scraper.py`, `fetcher.py`, `app.py`)

### 🧠 NLP Intelligence
- Summarize scraped text using Hugging Face Transformers (`BART-large`)
- Extract keywords using `KeyBERT` and `RAKE-NLTK`
- Visualize:
  - Word cloud of scraped text
  - Domain frequency histogram
  - Scraping success breakdown (planned)

### 📊 Output
- Download results as CSV or JSON
- Full log file saved as `scraper.log`

---

## 🖥️ Streamlit GUI Preview

- Set your query, count, and scraping mode from a sidebar
- View live scraping progress
- See results, summaries, keywords, and download buttons
- Analyze data right inside the app

---

## 📦 Project Structure

distributed-scraper/
├── app.py # Streamlit app with GUI + NLP
├── urls.txt # Sample URLs for local test
├── scraper.log # Log file with scraping records
├── requirements.txt # Python dependencies
└── src/
├── scraper.py # Core scraping logic (multiprocessing)
└── fetcher.py # DuckDuckGo search to get URLs

## 🛠️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/distributed-scraper.git
cd distributed-scraper

pip install -r requirements.txt
streamlit run app.py

