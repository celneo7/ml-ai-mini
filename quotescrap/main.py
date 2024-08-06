# codes referenced from geeksforgeeks
# https://www.geeksforgeeks.org/quote-guessing-game-using-web-scraping-in-python/

import requests
from bs4 import BeautifulSoup
from csv import writer, DictWriter
from time import sleep
from random import choice
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
    handlers=[
        logging.FileHandler("scraping.log"),  # Write log messages to a file
        logging.StreamHandler()  # Also output log messages to the console
    ]
)

url = "https://quotes.toscrape.com/"

# Function to read the last scraped page from the checkpoint file
def read_last_scraped_page():
    if os.path.exists("checkpoint.txt"):
        with open("checkpoint.txt", "r") as file:
            return int(file.read().strip())
    return 1

# Function to write the last scraped page to the checkpoint file
def write_last_scraped_page(page_number):
    with open("checkpoint.txt", "w") as file:
        file.write(str(page_number))


number = read_last_scraped_page()
page = f"/page/{number}/"

quotes = []

while url:

    try:
        res = requests.get(f"{url}{page}")  # Added timeout
        res.raise_for_status()  # Raise an error for bad responses
        logging.info(f"Scraping Page {number}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        break
        
    web = BeautifulSoup(res.text, "html.parser")

    q = web.find_all(class_ = "quote")


    with open("quotes.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = DictWriter(csvfile, fieldnames=["text", "author","link"])

        if csvfile.tell() == 0:
            writer.writeheader() #write header if file is empty

        for quote in q:
            new = {
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "link": quote.find("a")["href"]
            }

            writer.writerow(new)
            quotes.append(new)

            

            
    logging.info("Random quote: " + choice(quotes)["text"])
    quotes.clear()
    next = web.find(class_ = "next")
    page = next.find("a")["href"] if next else None

    if not next:
        logging.info("No next page found, ending scraping.")
        break


    sleep(2)

    number += 1
    write_last_scraped_page(number)

    





