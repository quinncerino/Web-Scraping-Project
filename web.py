import streamlit as st
import game_for_web
from random import choice
from time import sleep



def decrement_guesses():
    if st.session_state.remaining_guesses >= 0:
        st.session_state.remaining_guesses -= 1

    check_win_lose()
    if st.session_state.game_over == True:
        st.session_state.guess = ""


def new_round():
    st.session_state["quote"] = choice(quotes)
    st.session_state["remaining_guesses"] = 5
    st.session_state["game_over"] = False
    response.empty()
    win_message.empty()


def check_win_lose():
    if st.session_state["guess"].lower() == st.session_state.quote[1].lower():
        st.session_state.game_over = True
        response.info("That is correct! Congratulations, you've correctly guessed the author of the quote.")
        st.session_state.score += 1
        score_display.title(f"Score: {st.session_state.score}")
        if st.session_state.score == 10:
            win_message.markdown("Congratulations, you won the game!  \n:tada::fire::balloon::confetti_ball:  \nNew game loading. . .")
            sleep(4)
            st.session_state.score = 0
            response.info("Take your first guess above!")
            new_round()
        else:
            sleep(2)
            new_round()
    elif st.session_state.remaining_guesses == 0:
        st.session_state.game_over = True
        response.info(f"Sorry, that's incorrect! You ran out of guesses. The correct answer was: {name}")
        if st.session_state.score > 0:
            st.session_state.score -= 1
        score_display.title(f"Score: {st.session_state.score}")
        sleep(2)
        new_round()



st.set_page_config(layout = 'wide')


st.markdown(
    f"""<h1 style='
        color: {game_for_web.get_color()}; 
        font-family: "Verdana";
        font-size: 100px; 
        text-align: center;
        '>WORD FOR WORD</h1>""", 
        unsafe_allow_html=True)
 

col1, middle, col2 = st.columns([1.5, 0.1, 1.5])

with col1:
    st.image('images/whosaidquote.png')

with col2:
    st.title('"Who said that?!"')
    st.info("""\
            This is an interactive quote-guessing simulation. When given a quote, can you guess who said it, word for word?
            
            Each round, you will have 5 attempts to guess the person's name correctly.

            After each incorrect guess, you will receive a helpful hint!

            For each person you are able to guess correctly, you win that round and 1 point will be added to your score!

            If you run out of guesses, you lose that round and the answer will be provided. Your score will be deducted by 1 point.

            If you can achieve 10 points, then you win the game!""")




quotes = game_for_web.get_quotes_list("quotes.db")

if "quote" not in st.session_state:
    st.session_state.quote = choice(quotes)
    
if "remaining_guesses" not in st.session_state:
    st.session_state.remaining_guesses = 5

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "score" not in st.session_state:
    st.session_state.score = 0


quote = st.session_state.quote
name = quote[1]


col3, divider, col4 = st.columns([2, 0.1, 1])

with col3:
    st.header("Here's a quote:")
    st.write(quote[0])
    guess_made = st.text_input(label="Enter your guess:", key="guess", on_change=decrement_guesses)
    response = st.empty()

if st.session_state.get("guess"):
    response.info(game_for_web.make_guess(st.session_state.quote, st.session_state.remaining_guesses, st.session_state["guess"]))



with col4:
    score_display = st.title(f"Score: {st.session_state.score}")
    win_message = st.empty()
