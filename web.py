import streamlit as st
import game_for_web
from random import choice
from time import sleep



def decrement_guesses():
    if st.session_state.remaining_guesses >= 0:
        st.session_state.remaining_guesses -= 1
    print(st.session_state.remaining_guesses)
    check_win_lose()
    if st.session_state.game_over == True:
        st.session_state.guess = ""


def new_round():
    st.session_state["quote"] = choice(quotes)
    st.session_state["remaining_guesses"] = 5
    st.session_state["game_over"] = False


def check_win_lose():
    if st.session_state["guess"].lower() == st.session_state.quote[1].lower():
        st.session_state.game_over = True
        new_round()
    elif st.session_state.remaining_guesses == 0:
        st.session_state.game_over = True
        new_round()


st.set_page_config(layout = 'wide')


st.markdown(
    f"""<h1 style='
        color: {game_for_web.get_color()}; 
        font-family: "Optima";
        font-size: 100px; 
        text-align: center;
        '>WORD FOR WORD</h1>""", 
        unsafe_allow_html=True)
 

col1, middle, col2 = st.columns([1.5, 0.1, 1.5])

with col1:
    st.image('images/whosaidthat.jpg')

with col2:
    st.title('"Who said that?!"')
    st.info("""\
            This is an interactive quote-guessing simulation. When given a quote, can you guess who said it, word for word?
            
            Each round, you will have 5 attempts to guess the person's name correctly.

            After each incorrect guess, you will receive a helpful hint!

            If you run out of guesses, you lose and the answer will be provided. Your score will be reset to 0 points.

            If you can achieve 10 points by consecutively guessing ten correctly, then you win the game!""")



st.header("Here's a quote:")

quotes = game_for_web.get_quotes_list("quotes.db")

if "quote" not in st.session_state:
    st.session_state.quote = choice(quotes)
    
if "remaining_guesses" not in st.session_state:
    st.session_state.remaining_guesses = 5

if "game_over" not in st.session_state:
    st.session_state.game_over = False

quote = st.session_state.quote
st.write(quote[0])


guess_made = st.text_input(label="Enter your guess:", key="guess", on_change=decrement_guesses)



if st.session_state.get("guess"):
    st.info(game_for_web.make_guess(st.session_state.quote, st.session_state.remaining_guesses, st.session_state["guess"]))



