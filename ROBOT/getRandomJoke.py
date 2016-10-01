import random
import sqlite3

import praw

def getRandomJoke():
    conn = sqlite3.connect('Top_jokes.db')
    c = conn.cursor()
    numColumns = c.execute('SELECT COUNT(*) FROM Jokes_table').fetchone()[0]
    c.execute('SELECT Joke FROM Jokes_table WHERE id={sentenceId}'.\
            format(sentenceId=random.randint(1, numColumns))
            )
    return str(c.fetchone()[0])

print getRandomJoke()
