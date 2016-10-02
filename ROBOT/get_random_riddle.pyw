import random
import sqlite3
import markdown
import re

def get_random_riddle():
    try:
        conn = sqlite3.connect('jokes_and_riddles.db')
        c = conn.cursor()
        cc = conn.cursor()
        numRows = c.execute('SELECT COUNT(*) FROM riddle_table').fetchone()[0]
        Question = c.execute('SELECT Question FROM riddle_table WHERE id={sentenceId}'.\
                   format(sentenceId=random.randint(1, numRows))
                   )
        Answer = cc.execute('SELECT Answer FROM riddle_table WHERE id={sentenceId}'.\
                 format(sentenceId=random.randint(1, numRows))
                 )
        Question = cleanhtml( markdown.markdown(str(c.fetchone()[0])))
        Answer = cleanhtml( markdown.markdown(str(cc.fetchone()[0])))
        riddle = (Question, Answer)
        return riddle
    except:
        get_random_riddle()

def cleanhtml(raw_html):

    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html)
    return cleantext









