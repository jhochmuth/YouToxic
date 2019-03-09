from flask import flash, redirect, render_template, session, url_for

from youtoxic.app.context import app, pipeline
from youtoxic.app.forms import EnterTextForm, ReturnTweetsForm, TwitterAccountForm
from youtoxic.app.tweet_dumper import get_all_tweets, validate_username


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/enter_text', methods=['GET', 'POST'])
def enter_text():
    form = EnterTextForm()
    if form.validate_on_submit():
        if len(form.text.data.split()) < 3:
            flash('Warning: accuracy of predictions is low for texts with few words.')
        session['text'] = form.text.data
        session['types'] = form.types.data
        return redirect(url_for('result'))
    return render_template('enter_text.html', title='Enter Text', form=form)


@app.route('/twitter-credentials', methods=['GET'])
def get_twitter_credentials():
    form = TwitterAccountForm()
    return render_template('enter_twitter_username.html', title='Enter Twitter Username', form=form)


@app.route('/twitter-credentials', methods=['POST'])
def post_twitter_credentials():
    form = TwitterAccountForm()
    if form.validate_on_submit():
        if validate_username(form.user.data):
            session['username'] = form.user.data
            session['num_tweets'] = form.num_tweets.data
            session['types'] = form.types.data
            return redirect(url_for('return_tweets'))
        else:
            flash('Error: twitter account not found with specified username.')
            return redirect(url_for('post_twitter_credentials'))


@app.route('/result')
def result():
    preds = dict()
    classes = dict()
    pred_types = list()
    text = session['text']
    if 'toxic' in session['types']:
        preds['Toxicity'], classes['Toxicity'] = pipeline.predict_toxicity(text)
        pred_types.append('Toxicity')
    if 'identity' in session['types']:
        preds['Identity hate'], classes['Identity hate'] = pipeline.predict_identity_hate(text)
        pred_types.append('Identity hate')
    session.pop('text', None)
    session.pop('types', None)
    return render_template('result.html', title='Results', text=text, preds=preds, classes=classes, types=pred_types)


@app.route('/results_tweets')
def results_tweets():
    preds = dict()
    classes = dict()
    pred_types = list()
    username = session['username']
    num_tweets = session['num_tweets']
    display = session['display']
    session.pop('username', None)
    session.pop('num_tweets', None)
    session.pop('display', None)
    tweets = get_all_tweets(username, num_tweets=num_tweets)
    texts = [row[2] for row in tweets]
    if 'toxic' in session['types']:
        preds['Toxicity'], classes['Toxicity'] = pipeline.predict_toxicity_multiple(texts)
        pred_types.append('Toxicity')
    if 'identity' in session['types']:
        preds['Identity hate'], classes['Identity hate'] = pipeline.predict_identity_hate_multiple(texts)
        pred_types.append('Identity hate')
    return render_template('results_tweets.html', title='Results', tweets=tweets,
                           preds=preds, classes=classes, pred_types=pred_types, display=display)


@app.route('/return_tweets', methods=['GET', 'POST'])
def return_tweets():
    form = ReturnTweetsForm()
    username = session['username']
    num_tweets = session['num_tweets']
    tweets = get_all_tweets(username, num_tweets=num_tweets)
    if form.validate_on_submit():
        session['display'] = form.display.data
        return redirect(url_for('results_tweets'))
    return render_template('return_tweets.html', title='Tweets Posted by '+username,
                           form=form, tweets=tweets, username=username, num_tweets=num_tweets)
