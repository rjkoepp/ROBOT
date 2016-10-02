import sqlite3
import pandas
import praw

def main():
    USER_AGENT = 'Linux:scraper (by Winson)'
    r = praw.Reddit(USER_AGENT)
    conn = sqlite3.connect('jokes_and_riddles.db')
    c = conn.cursor()
    submissions = r.get_subreddit('riddles')
    post = submissions.get_top(params={'t': 'all'},limit = 25)
    counter = 0
    comment_start = 0
    for i in post:
        try:
            if 'reddit.com' not in i.url:
                raise ValueError('Skipping: Link Submission')
            riddle_question = i.title.encode('ascii', 'ignore').lower() + "\n" + i.selftext.encode('ascii', 'ignore').lower()
            riddle_answer = i.comments[0]
            counter = counter + 1
            print riddle_question
            print riddle_answer
            c.execute("INSERT INTO riddle_table VALUES (?,?,?)", (counter, str(riddle_question), str(riddle_answer)))
        except ValueError as err:
            print err
        except:
            pass
    conn.commit()
if __name__ == '__main__': main()
