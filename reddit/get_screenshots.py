from playwright.sync_api import sync_playwright

def get_screenshots(link="", comments=[]):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale="en-US")
        page = context.new_page()
        page.goto("https://www.reddit.com/r/AITAH/comments/1lwtz4h/aitah_for_telling_a_guy_to_shut_up_during_a_job/", wait_until="domcontentloaded")
        for id, _ in comments:
            full_id = f"t1_{id}"
            selector = f'div[id="{full_id}-comment-rtjson-content"]'
            print(selector)
            page.wait_for_selector(selector, timeout=10000)
            page.locator(selector).screenshot(path=f"./data/screenshots/{id}.png")
        browser.close()