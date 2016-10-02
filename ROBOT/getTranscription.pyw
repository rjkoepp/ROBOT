import pandas as pd
import praw

def get_transcription(x):
    r = praw.Reddit('YSK Scraper by /u/reffit_owner')
    submissions = r.get_subreddit('YouShouldKnow')
    posts = submissions.get_top(params={'t': 'all'}, limit=10)
    count = -1
    for i in posts:
        count += 1
        if count == x:
            print latin_to_mathematical(i.title)
            return ('You should know ' + i.title[4:], 'You should know ' + latin_to_mathematical(i.title)[4:])
    return None

def latin_to_mathematical(latinSentence):
    mathematicalSentence = ''
    keywords = pd.read_csv('LatinToMathematical.csv')

    latins = []
    for word in keywords['Latin']:
        latins.append(word)
    mathematicals = []
    for word in keywords['Mathematical']:
        mathematicals.append(word)

    for character in latinSentence:
        if character in latins:
            mathematicalSentence += mathematicals[latins.index(character)]
        else:
            mathematicalSentence += character.encode('utf-8')
    return mathematicalSentence.decode('utf-8')
