# 🎬 IMDb Movie Info Scraper (No API Required)

A lightweight Python project to fetch movie details from IMDb using an IMDb ID — **without relying on OMDb or paid APIs**. Uses `requests`, `BeautifulSoup`, and structured data from IMDb pages to extract info.

## 📦 Features

- Get detailed movie info using IMDb ID
- No need for API keys
- Saves structured JSON output
- Handles fallback extraction for country and language
- Works with dynamic layouts (IMDB's new/old structure)

## 🛠️ Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`

## 🚀 Installation

Clone this repository and set up a virtual environment:

```bash
git clone https://github.com/your-username/imdb-scraper.git
cd imdb-scraper

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
