from flask import Flask, render_template, request, redirect, url_for, session
import random

# Import the data from words.py
from words import words_list, stages, game_over

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session handling

# Reset and initialize game state
def reset_game(reset_streak=False):
    session['life'] = 6
    session['guessed_word_list'] = []
    session['chosen_word'] = random.choice(words_list)
    session['underscore_list'] = ["_"] * len(session['chosen_word'])
    session.setdefault('streak', 0)  # Set default streak value if not present
    if reset_streak:
        session['streak'] = 0

# Check if the user won
def check_win():
    return "_" not in session['underscore_list']

# Check if the user lost
def check_loss():
    return session['life'] <= 0

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize the game on first visit
    if 'chosen_word' not in session:
        session['streak'] = 0
        reset_game()

    if request.method == "POST":
        # Get the clicked letter from the button
        user_input = request.form.get("letter").upper()

        if user_input not in session['guessed_word_list']:
            session['guessed_word_list'].append(user_input)

            # Get all indices where the guessed letter matches
            char_index = [index for index, value in enumerate(session['chosen_word']) if value == user_input]
            underscore_list = list(session['underscore_list'])

            if not char_index:
                session['life'] -= 1  # Deduct life on wrong guess
            else:
                # Reveal the guessed letters in the underscore list
                for index in char_index:
                    underscore_list[index] = user_input

            # Update session data after processing the guess
            session['underscore_list'] = underscore_list

        # Check win/loss conditions
        if check_loss():
            rand_endings = random.randint(0, 4)
            session['streak'] = 0
            return render_template("index.html", game_over=True, life=session['life'], streak=session['streak'],
                                    uessed_word_list=session['guessed_word_list'], chosen_word=session['chosen_word'],
                                    message=game_over[rand_endings], underscore_list=session['underscore_list'],
                                    stages=stages[session['life']])

        elif check_win():
            session['streak'] += 1
            reset_game()
            return redirect(url_for('index'))

    return render_template("index.html", game_over=False, life=session['life'], streak=session['streak'],
                            guessed_word_list=session['guessed_word_list'], underscore_list=session['underscore_list'],
                            stages=stages[session['life']])


@app.route("/new_game")
def new_game():
    reset_game(reset_streak=True)  # Reset the game state and streak
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
