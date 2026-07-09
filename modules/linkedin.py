from playwright.sync_api import sync_playwright

def open_linkedin():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("https://www.linkedin.com/jobs")

        input("Login kar lo, phir Enter dabao...")

        page.goto("https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst")

        print("Data Analyst Jobs Opened")

        input("Press Enter to close...")

        browser.close()