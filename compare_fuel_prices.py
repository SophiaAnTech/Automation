import requests
from bs4 import BeautifulSoup

# replace this with a url that publishes fuel prices in your country
URL = "https://www.carsbruh.com/petrol-prices/"

# modify this accordingly based on the website you use
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# modify this based on how the fuel price is displayed on the website you are using
def get_ron95_prices():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    results = []
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) == 2:
                label = cells[0].get_text(strip=True)
                price = cells[1].get_text(strip=True)
                if "95" in label and price.startswith("$"):
                    station = label.split()[0]
                    price_value = float(price.replace("$", ""))
                    results.append((station, price_value))

    results.sort(key=lambda x: x[1])
    return results


prices = get_ron95_prices()

if len(prices) == 0:
    print("Could not fetch prices")
else:
    print("95 prices today (cheapest first):\n")
    for station, price in prices:
        print(station + ": $" + str(price))
