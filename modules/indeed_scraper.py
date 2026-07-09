import requests
from bs4 import BeautifulSoup


def scrape_indeed():

    url = "https://in.indeed.com/jobs?q=data+analyst"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "lxml")

    print("Page Title:", soup.title.text if soup.title else "No Title")