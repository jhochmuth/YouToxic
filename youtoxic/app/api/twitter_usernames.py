from flask import flash, redirect, render_template, session, url_for

from youtoxic.app.context import app
from youtoxic.app.forms import TwitterAccountForm
from youtoxic.app.tweet_dumper import validate_username


@app.route('/twitter-usernames', methods=['GET'])
def get_twitter_usernames():
    form = TwitterAccountForm()
    return render_template('enter_twitter_username.html', title='Enter Twitter Username', form=form)


@app.route('/twitter-usernames', methods=['POST'])
def post_twitter_usernames():
    form = TwitterAccountForm()
    if form.validate_on_submit():
        if validate_username(form.user.data):
            session['username'] = form.user.data
            session['num_tweets'] = form.num_tweets.data
            session['types'] = form.types.data
            return redirect(url_for('get_tweets'))
        else:
            flash('Error: twitter account not found with specified username.')
            return redirect(url_for('post_twitter_credentials'))
    return render_template('enter_twitter_username.html', title='Enter Twitter Username', form=form)
