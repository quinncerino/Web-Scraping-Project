import requests
from bs4 import BeautifulSoup
from time import sleep
import sqlite3


BASE_URL = "http://quotes.toscrape.com"


def scrape_quotes():
    all_quotes = []
    url = "/page/1"
    while url:
        res = requests.get(f"{BASE_URL}{url}")
        print(f"Now scraping: {BASE_URL}{url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            quote_data = (quote.find(class_="text").get_text(), quote.find(class_="author").get_text(), quote.find("a")["href"])
            all_quotes.append(quote_data)


        next_button = soup.find(class_="next")
        if next_button:
            url = next_button.find("a")["href"]
        else:
            break
        sleep(1)
    return all_quotes



def save_quotes(quotes):
    connection = sqlite3.connect('quotes.db')
    c = connection.cursor()

    # c.execute('''CREATE TABLE quotes 
    #         (statement TEXT, author TEXT, biolink TEXT)''')
    
    #c.executemany("INSERT INTO quotes VALUES (?,?,?)", quotes)

    connection.commit()
    connection.close()



quotes = scrape_quotes()
save_quotes(quotes)
