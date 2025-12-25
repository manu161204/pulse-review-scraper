from playwright.sync_api import sync_playwright


def scrape_trustradius(company_url):
    reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(company_url, timeout=60000)
        page.wait_for_timeout(5000)

        review_blocks = page.locator("div.review")

        for i in range(review_blocks.count()):
            text = review_blocks.nth(i).inner_text()
            reviews.append({"review": text})

        browser.close()

    return reviews
