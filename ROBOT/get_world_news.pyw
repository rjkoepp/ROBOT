import praw

def get_world_news(x = 1):
    r = praw.Reddit('worldgetter by /u/reffit_owner')
    submissions = r.get_subreddit('worldnews')
    posts = submissions.get_top(params={'t': 'hour'}, limit=x)
    news = []
    for i in posts:
        news.append(i.title + ": "  + i.url)
    return news
