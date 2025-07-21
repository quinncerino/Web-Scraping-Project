import requests
from bs4 import BeautifulSoup
from random import randint
import sqlite3

BASE_URL = "http://quotes.toscrape.com"

def get_color():
    colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "blueviolet", "cadetblue", "coral", "cornflowerblue", "darkcyan", "darkgreen", "darkmagenta", "darkorchid", "darkslateblue", "darkseagreen", "deeppink", "darkturquoise", "deepskyblue", "dodgerblue", "hotpink", "indianred", "indigo", "lightcoral", "lightpink", "lightseagreen", "lightgreen", "mediumorchid", "mediumpurple", "mediumvioletred", "mediumspringgreen", "mediumturquoise", "orchid", "palevioletred", "steelblue")

    choice = randint(0, len(colors)-1)
    clr = colors[choice]

    return clr


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
        return f"Sorry, that's incorrect! Here's a hint.  \nHint #1: This author was born on {soup.find(class_='author-born-date').get_text()} {soup.find(class_='author-born-location').get_text()}"
    elif remaining_guesses == 3:
        return f"Sorry, that's incorrect! Here's a hint.  \nHint #2: This author's first name starts with the letter '{name[0]}'"
    elif remaining_guesses == 2:
        space = name.rfind(' ')
        return f"Sorry, that's incorrect! Here's a hint.  \nHint #3: This author's last name starts with the letter '{name[space + 1]}'"
    elif remaining_guesses == 1:
        info = soup.find(class_='author-description').get_text()
        sections = name.split(' ')
        return f"Sorry, that's incorrect! Here's a hint. Hint #4: Here is more info about this author. {replace_info(info, sections)}"
    else:
        return "Take your first guess above!"
    # elif remaining_guesses == 0:
    #     return f"Sorry, that's incorrect!\nYou ran out of guesses. The correct answer was: {name}"
    # else:
    #     print(remaining_guesses)
    #     return "error"



def make_guess(quote, remaining_guesses, guess):
    name = quote[1]
    if guess.lower() == name.lower():
        return "That is correct! Congratulations, you've correctly guessed the author of the quote."

    if remaining_guesses >= 0:
        return print_hint(quote, remaining_guesses, name)
    else:
        return "Error"



# def start_game(quotes):
#     quote = choice(quotes)
#     remaining_guesses = 5
#     #get_color()
#     print("Here's a quote: ")
#     print(quote[0])
#     #print(quote['author'])
#     guess = ''
#     name = quote[1]

    # again = ''
    # while again.lower() not in ('y','yes','n','no'):
    #     again = input("Would you like to play again (Y/N)? ")
    # if again.lower() in ('y','yes'):
    #     print("\n")
    #     return start_game(quotes)
    # elif again.lower() in ('n', 'no'):
    #     print("Okay, goodbye!")


# def result_message(correct, remaining):
#     if correct == True:
#         return "\nThat is correct! Congratulations, you've correctly guessed the author of the quote."


#quotes = get_quotes_list("quotes.db")
#start_game(quotes)