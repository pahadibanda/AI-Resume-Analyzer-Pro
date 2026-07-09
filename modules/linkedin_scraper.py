from playwright.sync_api import sync_playwright


def open_jobs():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(
            "https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst"
        )

        input("Login ho jaye to Enter dabao...")

        print("Jobs Page Opened Successfully")

        input("Press Enter to close...")

        browser.close()