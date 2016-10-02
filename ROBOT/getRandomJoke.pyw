import random
import sqlite3

def get_random_joke():
    conn = sqlite3.connect('jokes_and_riddles.db')
    c = conn.cursor()
    numRows = c.execute('SELECT COUNT(*) FROM Jokes_table').fetchone()[0]
    c.execute('SELECT Joke FROM Jokes_table WHERE id={sentenceId}'.\
            format(sentenceId=random.randint(1, numRows))
            )
    joke = c.fetchone()
    return joke[0]
