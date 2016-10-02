from itertools import chain
import praw
import sqlite3
import pandas

def main():
    USER_AGENT = 'Linux:scraper (by Winson)'
    r = praw.Reddit(USER_AGENT)
    conn = sqlite3.connect('jokes_and_riddles.db')
    c = conn.cursor()
    submissions = r.get_subreddit('Jokes')
    post = chain(submissions.get_top(params={'t': 'all'},limit = None),
            submissions.get_top(params={'t': 'year'},limit = None))
    keywords = pandas.read_csv('censored_words.csv')
    for i in post:
        try:
            jokeString = i.title.encode('ascii', 'ignore').lower() + "\n" + i.selftext.encode('ascii', 'ignore').lower()
            jokeString = jokeString.decode('utf8')
            for word in keywords['Words'].dropna():
                if word in jokeString:
                    raise ValueError('CENSORED WORD FOUND')
            c.execute("INSERT INTO Jokes_table (Joke) VALUES (?)", (jokeString,))
            print jokeString
        except ValueError as err:
            print err

    conn.commit()
if __name__ == '__main__': main()
