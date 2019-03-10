from flask import render_template, session

from youtoxic.app.context import app, pipeline
from youtoxic.app.services.tweet_dumper import get_all_tweets


@app.route("/tweet-classifications", methods=["GET"])
def get_tweet_classifications():
    preds = dict()
    classes = dict()
    pred_types = list()
    username = session["username"]
    num_tweets = session["num_tweets"]
    display = session["display"]
    session.pop("username", None)
    session.pop("num_tweets", None)
    session.pop("display", None)
    tweets = get_all_tweets(username, num_tweets=num_tweets)
    texts = [row[2] for row in tweets]
    if "toxic" in session["types"]:
        preds["Toxicity"], classes["Toxicity"] = pipeline.predict_toxicity_multiple(
            texts
        )
        pred_types.append("Toxicity")
    if "identity" in session["types"]:
        preds["Identity hate"], classes[
            "Identity hate"
        ] = pipeline.predict_identity_hate_multiple(texts)
        pred_types.append("Identity hate")
    return render_template(
        "tweet_classifications.html",
        title="Results",
        tweets=tweets,
        preds=preds,
        classes=classes,
        pred_types=pred_types,
        display=display,
    )
