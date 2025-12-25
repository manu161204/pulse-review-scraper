# Pulse Review Scraper

Pulse Review Scraper is a Python-based web scraping project that extracts SaaS
product reviews from multiple platforms using **Playwright**.  
The project focuses on **robust scraping, clean data output, and real-world
error handling**, rather than fragile, hard-coded selectors.

---

## Features

- Scrapes product reviews from **Capterra** (primary source)
- Filters reviews using a configurable **date range**
- Handles **pagination safely** on SPA (Single Page Application) websites
- Exports structured review data in **JSON format**
- Includes **TrustRadius** as a bonus secondary source
- Works with **JavaScript-rendered pages**
- Uses **graceful failure handling** to avoid crashes on unstable pages

---

## Tech Stack

- Python 3.10+
- Playwright (browser automation)
- JSON for data storage

---

## Project Structure

pulse-review-scraper/
├── main.py # Main entry point
├── scraper/
│ └── trustradius_scraper.py # Bonus TrustRadius scraper
├── output/
│ └── reviews.json # Scraped review data
├── requirements.txt
└── README.md


---

## How to Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install
python main.py

---

Pagination Handling

Capterra is a React-based Single Page Application (SPA).
During pagination, the DOM is frequently re-mounted, which can invalidate
browser automation handles.

To ensure stability:

Pagination continues while the page remains stable

Pagination stops gracefully when instability is detected

This prevents crashes, infinite loops, and bot-detection issues

This approach reflects real-world web scraping best practices.

---

Note on G2 Reviews

G2 uses strong anti-bot protections (Cloudflare challenges) that block reliable
fully automated scraping.
Instead of forcing unstable scraping, this project documents the limitation
clearly and uses Capterra as the primary data source to ensure ethical and
reliable data collection.

---

Bonus: TrustRadius

A basic TrustRadius scraper is included to demonstrate extensibility and how
additional review sources can be integrated without affecting the core scraping
logic.

---x---


