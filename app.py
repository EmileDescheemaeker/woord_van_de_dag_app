from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('words.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS words
                    (id INTEGER PRIMARY KEY, word TEXT, definition TEXT,
                     example_sentence TEXT, date DATE)''')
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    word_of_the_day = conn.execute('SELECT * FROM words WHERE date = ?',
                                   (datetime.today().date(),)).fetchone()
    conn.close()
    return render_template('index.html', word=word_of_the_day)

@app.route('/add_word', methods=('GET', 'POST'))
def add_word():
    if request.method == 'POST':
        word = request.form['word']
        definition = request.form['definition']
        example_sentence = request.form['example_sentence']
        date = datetime.today().date()

        conn = get_db_connection()
        conn.execute('INSERT INTO words (word, definition, example_sentence, date) VALUES (?, ?, ?, ?)',
                     (word, definition, example_sentence, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_word.html')

@app.route('/view_words')
def view_words():
    conn = get_db_connection()
    words = conn.execute('SELECT * FROM words').fetchall()
    conn.close()
    return render_template('view_words.html', words=words)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

