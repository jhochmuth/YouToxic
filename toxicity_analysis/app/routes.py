from flask import flash, redirect, render_template, session, url_for

from toxicity_analysis.app.context import app
from toxicity_analysis.app.forms import EnterTextForm, TwitterAccountForm
from toxicity_analysis.app.predict_toxicity import predict_identity_hate, predict_toxicity, predict_toxicities
from toxicity_analysis.app.tweet_dumper import get_all_tweets, validate_username


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/enter_text', methods=['GET', 'POST'])
def enter_text():
    form = EnterTextForm()
    if form.validate_on_submit():
        if len(form.text.data.split()) < 3:
            flash('Warning: accuracy of predictions is low for texts with few words.')
        session['types'] = form.types.data
        return redirect(url_for('result', text=form.text.data))
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


@app.route('/result/<text>')
def result(text):
    preds = dict()
    classes = dict()
    pred_types = list()
    if 'toxic' in session['types']:
        preds['Toxicity'], classes['Toxicity'] = predict_toxicity(text)
        pred_types.append('Toxicity')
    if 'identity' in session['types']:
        preds['Identity hatred'], classes['Identity hatred'] = predict_identity_hate(text)
        pred_types.append('Identity hatred')
    session.pop('types', None)
    return render_template('result.html', title='Results', text=text, preds=preds, classes=classes, types=pred_types)


@app.route('/results_tweets/<username>/<num_tweets>')
def results_tweets(username, num_tweets):
    tweets = get_all_tweets(username, num_tweets=int(num_tweets))
    texts = [row[2] for row in tweets]
    preds, classifications = predict_toxicities(texts)
    for tweet, pred, classification in zip(tweets, preds, classifications):
        tweet.extend([pred, classification])
    return render_template('results_tweets.html', title='Results', tweets=tweets)


@app.route('/return_tweets/<username>/<num_tweets>')
def return_tweets(username, num_tweets):
    tweets = get_all_tweets(username, num_tweets=int(num_tweets))
    return render_template('return_tweets.html', title='Tweets Posted by '+username,
                           tweets=tweets, username=username, num_tweets=num_tweets)
