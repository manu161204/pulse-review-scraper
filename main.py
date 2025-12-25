from datetime import datetime
import json
import os
from playwright.sync_api import sync_playwright, TimeoutError
from scraper.trustradius_scraper import scrape_trustradius


def parse_date(date_text):
    try:
        return datetime.strptime(date_text, "%B %d, %Y")
    except:
        return None


def scrape_reviews_to_json():

    START_DATE = datetime(2010, 1, 1)
    END_DATE = datetime(2025, 12, 31)

    all_reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(
            "https://www.capterra.com/p/155103/Salesforce-Sales-Cloud/",
            timeout=60000
        )


        page.mouse.wheel(0, 5000)

        try:
            page.wait_for_selector("div:has-text('Pros')", timeout=15000)
        except TimeoutError:
            print("❌ Reviews did not load")
            browser.close()
            return

       
        while True:

            page.mouse.wheel(0, 5000)
            page.wait_for_timeout(4000)

            review_blocks = page.locator("div:has-text('Pros')")
            total = review_blocks.count()

            print(f"Scraping {total} reviews from current page...")

            if total == 0:
                break

            for i in range(total):
                review = review_blocks.nth(i)

                
                try:
                    date = review.locator(
                        "text=/\\w+ \\d{1,2}, \\d{4}/"
                    ).first.inner_text()
                except:
                    date = "N/A"

                
                try:
                    pros = review.locator(
                        "xpath=.//*[text()='Pros']/following::p"
                    ).first.inner_text()
                except:
                    pros = "N/A"

            
                try:
                    cons = review.locator(
                        "xpath=.//*[text()='Cons']/following::p"
                    ).first.inner_text()
                except:
                    cons = "N/A"

                parsed_date = parse_date(date)

                if parsed_date and START_DATE <= parsed_date <= END_DATE:
                    all_reviews.append({
                        "date": date,
                        "pros": pros,
                        "cons": cons
                    })

            # NEXT BUTTON (ULTRA-SAFE PLAYWRIGHT EDGE-CASE HANDLING)
            try:
                next_button = page.query_selector("button:has-text('Next')")
            except Exception:
                print("Page became unstable. Stopping pagination.")
                break

            if not next_button:
                print("No more pages. Pagination finished.")
                break

            try:
                next_button.click()
                page.wait_for_timeout(5000)
            except Exception:
                print("Navigation caused page reset. Ending pagination.")
                break

        browser.close()

    
    os.makedirs("output", exist_ok=True)

    with open("output/reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(all_reviews)} reviews saved to output/reviews.json")


if __name__ == "__main__":
    scrape_reviews_to_json()

    
    tr_reviews = scrape_trustradius(
        "https://www.trustradius.com/products/salesforce-sales-cloud/reviews"
    )

    print(f"✅ {len(tr_reviews)} TrustRadius reviews scraped")

