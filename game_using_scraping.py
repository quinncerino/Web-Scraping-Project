import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from pyfiglet import figlet_format
from termcolor import colored
from random import randint

def show_title():
    colors = ("red", "green", "yellow", "blue", "magenta", "cyan")

    choice = randint(0, 5)
    clr = colors[choice]

    text = figlet_format("Quizzical Quotes", font="big")
    print("\n")
    print(colored(text, clr))


def replace_info(string, sections):
    if len(sections) == 0:
        return string
    else:
        return replace_info(string.replace(sections[-1], "_______"), sections[:-1])


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
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")["href"]
            })


        next_button = soup.find(class_="next")
        if next_button:
            url = next_button.find("a")["href"]
        else:
            break
        #sleep(1)
    return all_quotes


def print_hint(quote, remaining_guesses, name):
    res = requests.get(f"{BASE_URL}{quote['bio-link']}")
    soup = BeautifulSoup(res.text, "html.parser")
    if remaining_guesses == 4:
        print(f"Hint #1: This author was born on {soup.find(class_='author-born-date').get_text()} {soup.find(class_='author-born-location').get_text()}\n")
    elif remaining_guesses == 3:
        print(f"Hint #2: This author's first name starts with the letter '{name[0]}'\n")
    elif remaining_guesses == 2:
        space = name.rfind(' ')
        print(f"Hint #3: This author's last name starts with the letter '{name[space + 1]}'\n")
    elif remaining_guesses == 1:
        print(f"Hint #4: Here is more info about this author.")
        info = soup.find(class_='author-description').get_text()
        sections = name.split(' ')
        print(replace_info(info, sections))
    else:
        print(f"You ran out of guesses. The answer was: {name}")



def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 5
    show_title()
    print("Here's a quote: ")
    print(quote['text'])
    #print(quote['author'])
    guess = ''
    name = quote['author']

    while remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
        if guess.lower() == name.lower():
            print("\nThat is correct! Congratulations, you've correctly guessed the author of the quote.")
            break

        remaining_guesses -= 1
        if remaining_guesses >= 1:
            print("Sorry, that's incorrect! Here's a hint:\n")
        else:
            print("Sorry, that's incorrect!\n")

        print_hint(quote, remaining_guesses, name)


    again = ''
    while again.lower() not in ('y','yes','n','no'):
        again = input("Would you like to play again (Y/N)? ")
    if again.lower() in ('y','yes'):
        print("\n")
        return start_game(quotes)
    elif again.lower() in ('n', 'no'):
        print("Okay, goodbye!")


quotes = scrape_quotes()
start_game(quotes)