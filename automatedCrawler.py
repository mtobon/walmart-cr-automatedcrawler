import time
import csv
from datetime import datetime
from playwright.sync_api import sync_playwright

def run_full_category_crawler(category_url):
    with sync_playwright() as p:
        print("🚀 Starting the Master Crawler Engine...")
        
        browser = p.chromium.launch(
            channel="msedge", 
            headless=False,
            args=["--disable-features=Translate", "--no-first-run", "--disable-infobars"]
        )
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            extra_http_headers={"Accept-Language": "es-CR,es;q=0.9,en;q=0.8"}
        )
        page = context.new_page()

        # ==========================================
        # PHASE 1: COLLECT EVERY SINGLE LINK
        # ==========================================
        print(f"\n🕵️‍♂️ PHASE 1: Scanning category page: {category_url}")
        page.goto(category_url, wait_until="domcontentloaded", timeout=60000)
        
        print("📜 Scrolling and clicking 'Mostrar más' to load ALL products...")
        
        # We will try to click the "Show More" button up to 10 times.
        # This ensures we get a massive list of Products.
        for i in range(10):
            # Scroll to the bottom of the current list
            page.mouse.wheel(0, 3000)
            time.sleep(2)
            
            try:
                # VTEX usually uses a button that says "Mostrar más" (Show More)
                # We tell Playwright to look for any button containing that text
                show_more_btn = page.locator("button:has-text('Mostrar más')").first
                
                if show_more_btn.is_visible(timeout=3000):
                    print(f"   👉 Clicking 'Mostrar más' (Page {i+2})...")
                    show_more_btn.click()
                    time.sleep(4) # Give the new Products time to load onto the screen
                else:
                    print("   🛑 Reached the bottom of the category!")
                    break # Break out of the loop if the button is gone
            except Exception:
                break # If there's an error finding the button, we assume we're at the end

        # Now that everything is loaded, grab all the links!
        link_elements = page.locator("a[href$='/p']").all()
        product_urls = set()
        
        for el in link_elements:
            href = el.get_attribute("href")
            if href:
                if href.startswith("/"):
                    #Target
                    href = "https://www.walmart.co.cr" + href
                product_urls.add(href)

        urls_to_scrape = list(product_urls)
        print(f"\n🎯 BOOM! Found {len(urls_to_scrape)} unique Products across the whole category!")

        # ==========================================
        # PHASE 2: SCRAPE AND SAVE TO EXCEL
        # ==========================================
        print(f"\n🚜 PHASE 2: Beginning bulk data extraction...")
        
        for index, url in enumerate(urls_to_scrape, start=1):
            print(f"\n🔄 [{index}/{len(urls_to_scrape)}] Checking: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                price_locator = page.locator(".vtex-store-components-3-x-currencyContainer").first
                price_locator.wait_for(timeout=10000) 
                price = price_locator.inner_text()
                
                title_locator = page.locator("h1").first
                title = title_locator.inner_text() if title_locator.count() > 0 else "Unknown Product"

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"✅ SAVED: {title} | {price}")
                
                with open('walmart_prices.csv', mode='a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_time, title, price, url])
                    
            except Exception as e:
                print(f"⚠️ Failed to scrape. Skipping... ({e})")

            time.sleep(2) # Anti-bot rest period

        print("\n🎉 ALL DONE! Your spreadsheet is fully stocked. Closing browser.")
        browser.close()

# Your specific category link!
main_category_link = "https://www.walmart.co.cr/1379?map=productClusterIds"
run_full_category_crawler(main_category_link)