from flask import flash, redirect, render_template, url_for

from toxicity_analysis.app.context import app
from toxicity_analysis.app.forms import EnterTextForm, TwitterAccountForm
from toxicity_analysis.app.predict_toxicity import predict_toxicity
from toxicity_analysis.app.tweet_dumper import get_all_tweets, validate_username


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/enter_text', methods=['GET', 'POST'])
def enter_text():
    form = EnterTextForm()
    if form.validate_on_submit():
        if len(form.text.data.split()) < 3:
            flash('Warning: accuracy of predictions is low for text with few words.')
        return redirect(url_for('results', text=form.text.data))
    return render_template('enter_text.html', title='Enter Text', form=form)


@app.route('/enter_twitter_username', methods=['GET', 'POST'])
def enter_twitter_username():
    form = TwitterAccountForm()
    if form.validate_on_submit():
        if validate_username(form.text.data):
            return redirect(url_for('return_tweets', username=form.text.data))
        else:
            flash('Error: twitter account not found with specified username.')
            return redirect(url_for('enter_twitter_username'))
    return render_template('enter_twitter_username.html', title='Enter Twitter Username', form=form)


@app.route('/results/<text>')
def results(text):
    prediction = predict_toxicity(text)
    return render_template('results.html', title='Results', text=text, prediction=prediction)


@app.route('/return_tweets/<username>')
def return_tweets(username):
    tweets = get_all_tweets(username, max_tweets=10)
    return render_template('return_tweets.html', title='Tweets Posted by ' + username, tweets=tweets)
