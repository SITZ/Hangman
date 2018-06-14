from random import randint
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

MAX_INCORRECT_GUESS_COUNT = 5
POSSIBLE_GUESSES = set('abcdefghijklmnopqrstuvwxyz1234567890')

hangmans = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
max_score = 0

hangman_internal = list(hangmans[randint(0, len(hangmans) - 1)])
hangman_external = ['_'] * len(hangman_internal)
incorrect_guesses = set()
all_guesses = set()


@app.route('/', methods=['GET'])
def index():
    return render_template(
        'hangman.html',
        hangman_external=hangman_external,
        max_score=max_score,
        life_lines=MAX_INCORRECT_GUESS_COUNT - len(incorrect_guesses),
        all_guesses=all_guesses
    )


@app.route('/guess/<string:input>', methods=['POST'])
def guess(input):
    global incorrect_guesses, hangman_external, hangman_internal, max_score

    if input not in POSSIBLE_GUESSES:
        pass
    elif input in incorrect_guesses:
        pass
    elif input not in hangman_internal:
        incorrect_guesses.add(input)
        all_guesses.add(input)
    else:
        for index, char in enumerate(hangman_internal):
            if char == input:
                hangman_external[index] = hangman_internal[index]
        all_guesses.add(input)

    if len(incorrect_guesses) >= MAX_INCORRECT_GUESS_COUNT:
        all_guesses.update(POSSIBLE_GUESSES)
    elif len(set(hangman_external).intersection(set(hangman_internal))) == len(hangman_internal):
        max_score = max(max_score, MAX_INCORRECT_GUESS_COUNT - len(incorrect_guesses))
        all_guesses.update(POSSIBLE_GUESSES)

    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset():
    global hangman_internal, hangman_external, incorrect_guesses, all_guesses

    hangman_internal = list(hangmans[randint(0, len(hangmans) - 1)])
    hangman_external = ['_'] * len(hangman_internal)

    incorrect_guesses = set()
    all_guesses = set()

    return redirect(url_for('index'))


@app.route('/api', methods=['GET'])
def api():
    return render_template('api.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
