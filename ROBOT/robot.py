from _future_ import print_function

import configparser
import praw

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    USER_AGENT = config.get('praw', 'USER_AGENT')

    r = praw.Reddit(USER_AGENT)

    while True:
        o.refresh()
         











