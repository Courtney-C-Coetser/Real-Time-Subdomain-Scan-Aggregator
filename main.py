import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask
import os

app = Flask(__name__)
file_path = "output.txt"

def scrape_loop():
    while True:
        try:
            r = requests.get("https://subdomainfinder.c99.nl/overview")
            soup = BeautifulSoup(r.text, 'html.parser')
            history_items = soup.find_all("div", class_='history-item')
            new_items = [item.get_text(strip=True) for item in history_items]

            try:
                with open(file_path, 'r') as f:
                    existing_items = set(line.strip() for line in f.readlines())
            except FileNotFoundError:
                existing_items = set()

            items_to_add = [item for item in new_items if item not in existing_items]

            if items_to_add:
                with open(file_path, 'a') as f:
                    for item in items_to_add:
                        f.write(item + '\n')
                print(f"Added {len(items_to_add)} new items.")
            else:
                print("No new items to add.")

            time.sleep(10)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

threading.Thread(target=scrape_loop, daemon=True).start()

@app.route("/")
def index():
    return "Subdomain scraper is running.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
