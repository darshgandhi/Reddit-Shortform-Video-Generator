from playwright.sync_api import sync_playwright

def get_screenshots(link="", comments=[], screenshot=False):
    if not screenshot: 
        return False
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale="en-US")
        page = context.new_page()
        try:
            page.goto(link, wait_until="domcontentloaded")
            for id, _ in comments:
                full_id = f"t1_{id}"
                selector = f'div[id="{full_id}-comment-rtjson-content"]'
                print(selector)
                page.wait_for_selector(selector, timeout=10000)
                page.locator(selector).screenshot(path=f"./data/screenshots/{id}.png")
            browser.close()
            return True
        except:
            print("Screenshotting failed...")
            browser.close()
            return False