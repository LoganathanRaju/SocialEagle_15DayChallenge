from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus
import os
import requests
from urllib.parse import urljoin

QUERY = "indian rupee vs singapore dollar history"

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Firefox avoids detection
        page = browser.new_page()

        # Search on Bing
        search_url = f"https://www.bing.com/search?q={quote_plus(QUERY)}"
        page.goto(search_url)
        page.wait_for_selector("li.b_algo h2 a")

        # Click first result
        first_link = page.query_selector("li.b_algo h2 a")
        if not first_link:
            print("❌ No search result found.")
            browser.close()
            return
        first_link.click()
        page.wait_for_load_state("networkidle")

        # ✅ Save text
        text = page.evaluate("() => document.body.innerText")
        with open("data3.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ Text saved to data3.txt")

        # ✅ Capture infographics (images)
        os.makedirs("data3_images", exist_ok=True)
        img_elements = page.query_selector_all("img")

        count = 1
        for img in img_elements:
            src = img.get_attribute("src")
            if not src:
                continue

            # Handle relative links
            src = urljoin(page.url, src)

            try:
                r = requests.get(src, timeout=10)
                if r.status_code == 200 and r.content:
                    ext = ".jpg"
                    if ".png" in src:
                        ext = ".png"
                    elif ".svg" in src:
                        ext = ".svg"

                    filename = f"data3_{count}{ext}"
                    filepath = os.path.join("data3_images", filename)

                    with open(filepath, "wb") as f:
                        f.write(r.content)
                    print(f"✅ Saved {filename}")
                    count += 1
            except Exception as e:
                print(f"⚠️ Could not save {src}: {e}")

        browser.close()

if __name__ == "__main__":
    main()
