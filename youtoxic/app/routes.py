from flask import render_template

import youtoxic.app.api.text_classifications
import youtoxic.app.api.texts
import youtoxic.app.api.tweet_classifications
import youtoxic.app.api.tweets
import youtoxic.app.api.twitter_usernames
from youtoxic.app.context import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home')
