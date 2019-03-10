from flask import redirect, render_template, session, url_for

from youtoxic.app.api.forms import ReturnTweetsForm
from youtoxic.app.context import app
from youtoxic.app.services.tweet_dumper import get_all_tweets


@app.route("/tweets", methods=["GET"])
def get_tweets():
    form = ReturnTweetsForm()
    username = session["username"]
    num_tweets = session["num_tweets"]
    tweets = get_all_tweets(username, num_tweets=num_tweets)
    return render_template(
        "return_tweets.html",
        title="Tweets Posted by " + username,
        form=form,
        tweets=tweets,
        username=username,
        num_tweets=num_tweets,
    )


@app.route("/tweets", methods=["POST"])
def post_tweets():
    form = ReturnTweetsForm()
    if form.validate_on_submit():
        session["display"] = form.display.data
        return redirect(url_for("get_tweet_classifications"))
