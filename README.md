# Walmart Costa Rica - Automated Product Crawler 🚜🛒

A robust, automated web scraping solution built with **Python** and **Playwright** designed to extract product data from Walmart Costa Rica's e-commerce platform.

## 🌟 Features

* [cite_start]**VTEX Architecture Compatibility**: Specifically engineered to navigate and scrape stores built on the VTEX platform[cite: 17, 18, 22].
* [cite_start]**Dynamic Loading Handling**: Automatically scrolls and interacts with "Mostrar más" (Show More) buttons to ensure full category indexing[cite: 21, 23].
* **Two-Phase Execution**:
    1.  [cite_start]**Phase 1 (Discovery)**: Scans category pages to collect all unique product URLs[cite: 19, 25].
    2.  [cite_start]**Phase 2 (Extraction)**: Visits each product page to extract real-time titles and prices[cite: 27, 28, 29].
* [cite_start]**Anti-Bot Resilience**: Implements custom User-Agents, viewport configurations, and rest periods to mimic human behavior[cite: 18, 31].
* [cite_start]**Automated Data Export**: Saves all results into a clean, UTF-8 encoded `walmart_prices.csv` file with timestamps.

## 🛠️ Tech Stack

* **Language**: Python 3.x
* [cite_start]**Automation**: [Playwright](https://playwright.dev/) [cite: 16, 17]
* [cite_start]**Browser Engine**: Chromium (Microsoft Edge channel) [cite: 17]
* [cite_start]**Data Handling**: CSV & Datetime modules [cite: 17]

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed, then clone this repository and install the dependencies:

```bash
# Install required libraries
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install


Usage
Simply run the main script to start the crawling process:
python automatedCrawler.py

The script is currently configured to scan a specific category cluster but can be modified by changing the main_category_link variable in the code.

📊 Output Data

The crawler generates a walmart_prices.csv containing:
Timestamp: Precise date and time of the scrape.
Product Title: Full name of the item.
Price: Current price displayed on the store.
URL: Direct link to the product.

Disclaimer: This project is for educational purposes only. Always check the website's robots.txt and terms of service before scraping.