# YTScraper

YTScraper is a Python-based web scraper that extracts video titles from YouTube channels using Selenium.

## Features
- Scrapes video titles, upload date and views from specified YouTube channels.
- Automatically scrolls through the video list to load more content.
- Handles page loading and timeout errors.

## Requirements
- Python 
- ChromeDriver
- Required Python packages:
  - Selenium
  - webdriver-manager

## Installation and Usage

1. **Clone this repository**:
   ```bash
   git clone https://github.com/kostonks/YTScraper.git
   cd YTScraper
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper**:
   Update the `urls` list in `main.py` with the YouTube channel URLs you want to scrape, then execute the script:
   ```bash
   python main.py
   ```


