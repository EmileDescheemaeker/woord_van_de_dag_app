import csv
import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('words.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_words_from_csv(file_path):
    conn = get_db_connection()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row['word']
            definition = row['definition']
            example_sentence = row['example_sentence']
            date = datetime.today().date()
            conn.execute('INSERT INTO words (word, definition, example_sentence, date) VALUES (?, ?, ?, ?)',
                         (word, definition, example_sentence, date))
        conn.commit()
    conn.close()

if __name__ == '__main__':
    add_words_from_csv('words.csv')
    print("Woorden zijn succesvol toegevoegd aan de database.")
