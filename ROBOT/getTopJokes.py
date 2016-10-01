import praw

def getTopJokes(x):
    r = praw.Reddit('jokegetter by /u/reffit_owner')
    submissions = r.get_subreddit('Jokes')
    posts = submissions.get_top(params={'t': 'hour'}, limit=x)
    jokes = []
    for i in posts:
        jokes.append(i.title + "\n" + i.selftext)
    return jokes
