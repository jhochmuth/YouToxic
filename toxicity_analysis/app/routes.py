from flask import flash, redirect, render_template, url_for

from toxicity_analysis.app.context import app
from toxicity_analysis.app.forms import EnterTextForm, TwitterAccountForm
from toxicity_analysis.app.predict_toxicity import predict_toxicity, predict_toxicities
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
        if validate_username(form.user.data):
            return redirect(url_for('return_tweets', username=form.user.data, num_tweets=form.num_tweets.data))
        else:
            flash('Error: twitter account not found with specified username.')
            return redirect(url_for('enter_twitter_username'))
    return render_template('enter_twitter_username.html', title='Enter Twitter Username', form=form)


@app.route('/results/<text>')
def results(text):
    prediction = predict_toxicity(text)
    return render_template('results.html', title='Results', text=text, prediction=prediction)


@app.route('/results_tweets/<username>/<num_tweets>')
def results_tweets(username, num_tweets):
    tweets = get_all_tweets(username, num_tweets=int(num_tweets))
    texts = [row[2] for row in tweets]
    predictions = predict_toxicities(texts)
    for tweet, prediction in zip(tweets, predictions):
        tweet.append(prediction)
    return render_template('results_tweets.html', title='Results', tweets=tweets)


@app.route('/return_tweets/<username>/<num_tweets>')
def return_tweets(username, num_tweets):
    tweets = get_all_tweets(username, num_tweets=int(num_tweets))
    return render_template('return_tweets.html', title='Tweets Posted by '+username,
                           tweets=tweets, username=username, num_tweets=num_tweets)
