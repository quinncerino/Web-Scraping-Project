import requests
from bs4 import BeautifulSoup
from random import choice
from pyfiglet import figlet_format
from termcolor import colored
from random import randint
import sqlite3

BASE_URL = "http://quotes.toscrape.com"

def show_title():
    colors = ("red", "green", "yellow", "blue", "magenta", "cyan")

    choice = randint(0, 5)
    clr = colors[choice]

    text = figlet_format("Quizzical Quotes", font="big")
    print("\n")
    print(colored(text, clr))


def get_quotes_list(filename):
    connection = sqlite3.connect(filename)
    c = connection.cursor()
    c.execute("SELECT * FROM quotes")
    quotes_list = c.fetchall()
    connection.commit()
    connection.close()
    return quotes_list


def replace_info(string, sections):
    if len(sections) == 0:
        return string
    else:
        return replace_info(string.replace(sections[-1], "_______"), sections[:-1])


def print_hint(quote, remaining_guesses, name):
    res = requests.get(f"{BASE_URL}{quote[2]}")
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
    print(quote[0])
    #print(quote['author'])
    guess = ''
    name = quote[1]

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


quotes = get_quotes_list("quotes.db")
start_game(quotes)