from flask import Flask, render_template, request, redirect, url_for
import random

# Import the data from words.py
from words import starting_logo, words_list, stages, game_over

app = Flask(__name__)

# Initialize the game variables
life = 6
streak = 0
guessed_word_list = []
chosen_word = ""
underscore_list = []

# Reset and initialize game state
def reset_game():
    global life, streak, guessed_word_list, chosen_word, underscore_list
    life = 6
    guessed_word_list = []
    chosen_word = random.choice(words_list)
    underscore_list = ["_"] * len(chosen_word)

@app.route("/", methods=["GET", "POST"])
def index():
    global life, streak, guessed_word_list, chosen_word, underscore_list

    # Start new game if it's the first visit
    if chosen_word == "":
        reset_game()

    if request.method == "POST":
        # Get the clicked letter from the button
        user_input = request.form.get("letter").upper()

        if user_input not in guessed_word_list:
            guessed_word_list.append(user_input)
            char_index = [index for index, value in enumerate(chosen_word) if value == user_input]

            # Deduct life if the guess is incorrect
            if not char_index:
                life -= 1

            # Reveal guessed character
            for index in char_index:
                underscore_list[index] = user_input

        # Check for win/loss conditions
        if life <= 0:
            rand_endings = random.randint(0, 4)
            return render_template("index.html", game_over=True, life=life, streak=streak, guessed_word_list=guessed_word_list,
                                    chosen_word=chosen_word, message=game_over[rand_endings], underscore_list=underscore_list,
                                    stages=stages[life])

        if "_" not in underscore_list:
            streak += 1
            reset_game()
            return redirect(url_for('index'))

    return render_template("index.html", game_over=False, life=life, streak=streak, guessed_word_list=guessed_word_list,
                            underscore_list=underscore_list, stages=stages[life])

@app.route("/new_game")
def new_game():
    reset_game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
