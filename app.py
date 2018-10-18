
import shutil

import pandas as pd
from flask import Flask, render_template
from pony.orm import *
import db_init

app = Flask(__name__)

@app.route('/')
@db_session
def index():
    total_space, used_space, free_space = shutil.disk_usage(__file__)
    total_tweets = count_tweets()
    last_five_tweets = find_last_tweets()
    print(last_five_tweets)
    return render_template('index.html',
        last_tweets=last_five_tweets, 
        total=total_tweets, 
        space = total_space/10 **9,
        used = used_space/10**9,
        free = free_space/10**9 )


def find_last_tweets():
    return db_init.Tweet.select().order_by(desc(db_init.Tweet.created_at))[:5]



def count_tweets():
    return select((count(t)) for t in db_init.Tweet)[:1]



if __name__ == '__main__':
    app.run(port=443, host='0.0.0.0')
