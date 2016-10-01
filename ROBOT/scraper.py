import praw
import sqlite3


def main():
    USER_AGENT = 'Linux:scraper (by Winson)'
    r = praw.Reddit(USER_AGENT)
    conn = sqlite3.connect('Top_jokes.db')
    c = conn.cursor()
    submissions = r.get_subreddit('Jokes')
    post = submissions.get_top(params={'t': 'all'},limit = None)
    print c.execute("SELECT * FROM Jokes_table")
    for i in post:
        jokeString = i.title.encode('ascii', 'ignore').lower() + "\n" + i.selftext.encode('ascii', 'ignore').lower()
        jokeString = jokeString.decode('utf8')
        print jokeString
        c.execute("INSERT INTO Jokes_table (Joke) VALUES (?)", (jokeString,))

    conn.commit()
if __name__ == '__main__': main()
