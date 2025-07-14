import requests
from bs4 import BeautifulSoup
import schedule
import time


def check_amazon_stock(url):
    """Check Amazon product page for availability."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Error fetching {url}: {exc}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract product name
    title_el = soup.find(id="productTitle")
    title = title_el.get_text(strip=True) if title_el else "Unknown"

    # Extract price if available
    price_el = soup.find(id="priceblock_ourprice") or soup.find(id="priceblock_dealprice")
    price = price_el.get_text(strip=True) if price_el else "-"

    # Determine stock status
    availability_el = soup.find(id="availability")
    in_stock = availability_el and "在庫あり" in availability_el.get_text()

    if in_stock:
        print(f"[AMAZON] {title} {price} {url}")


def job():
    check_amazon_stock("https://amzn.asia/d/eqWwDwc")


if __name__ == "__main__":
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

