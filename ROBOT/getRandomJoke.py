import random
import sqlite3

def getRandomJoke():
    conn = sqlite3.connect('Top_jokes.db')
    c = conn.cursor()
    numRows = c.execute('SELECT COUNT(*) FROM Jokes_table').fetchone()[0]
    c.execute('SELECT Joke FROM Jokes_table WHERE id={sentenceId}'.\
            format(sentenceId=random.randint(1, numRows))
            )
    return str(c.fetchone()[0])

print getRandomJoke()
