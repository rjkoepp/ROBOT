import praw

def get_top_jokes(posts = 1):
    r = praw.Reddit('jokegetter by /u/reffit_owner')
    submissions = r.get_subreddit('Jokes')
    posts = submissions.get_top(params={'t': 'hour'}, limit=posts)
    jokes = []
    for i in posts:
        jokes.append(i.title + "\n" + i.selftext)
    if len(jokes) == 1:
        return jokes[0]
    
    return jokes
