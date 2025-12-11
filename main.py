import time
import requests
from bs4 import BeautifulSoup

file_path = "output.txt"

def main_task():
    print("Script is running...")

    # Fetch page
    r = requests.get("https://subdomainfinder.c99.nl/overview")
    soup = BeautifulSoup(r.text, 'html.parser')

    # Extract all history items
    history_items = soup.find_all("div", class_='history-item')
    new_items = [item.get_text(strip=True) for item in history_items]

    # Read existing items from file
    try:
        with open(file_path, 'r') as f:
            existing_items = set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        existing_items = set()  # If file doesn't exist yet

    # Filter out already existing items
    items_to_add = [item for item in new_items if item not in existing_items]

    if items_to_add:
        # Append only new items to the file
        with open(file_path, 'a') as f:
            for item in items_to_add:
                f.write(item + '\n')
        print(f"Added {len(items_to_add)} new items.")
    else:
        print("No new items to add.")

    time.sleep(10)


if __name__ == "__main__":
    while True:
        try:
            main_task()
        except KeyboardInterrupt:
            print("\nScript stopped manually.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
