"""For predicting the toxicities of tweets of a specified Twitter user."""

import dash_core_components as dcc

import dash_html_components as html

import dash_table

from dateutil import parser

import pandas as pd

from youtoxic.app.services.tweet_dumper import (
    get_tweets,
    get_tweets_by_date,
    validate_username,
)


def get_tweet_predictions(
    username, num_tweets, types, limit_date, start_date, end_date, pipeline
):
    """Returns the toxicity predictions for tweets of a specified twitter user.

    Parameters
    ----------
    username: str
        The Twitter user to collect tweets from.

    num_tweets: int
        The maximum number of tweets to analyze.

    types: List
        The types of toxicity to predict for.

    limit_date: str
        Whether to get tweets between a certain date range ('date') or the most recent tweets ('all').

    start_date: Datetime
        Minimum date for date-limited collection. Only matters if limit_date == 'date'.

    end_date: Datetime
        Maximum date for date-limited collection. Only matters if limit_date == 'date'.

    pipeline: Object
        The pipeline object used to make predictions.

    Returns
    -------
        The html layout for the subsection of the page that contains results.

    """
    if username.lower() == "realdonaldtrump":
        return html.Div(
            "Is that really necessary? It is obvious that all those tweets "
            "will include every type of toxicity known to mankind.",
            style={"color": "rgb(255, 0, 0"},
        )
    if limit_date == "date" and (not start_date or not end_date):
        return html.Div(
            "Error: You must specify a date range if selecting to limit by date.",
            style={"color": "rgb(255, 0, 0"},
        )
    if not types:
        return html.Div(
            "Error: You must select at least one type of toxicity.",
            style={"color": "rgb(255, 0, 0"},
        )

    if not validate_username(username):
        return html.Div(
            "Error: Could not find Twitter account associated with that name.",
            style={"color": "rgb(255, 0, 0"},
        )

    if limit_date == "all":
        tweets = get_tweets(username, num_tweets)
    else:
        start_date = parser.parse(start_date).date()
        end_date = parser.parse(end_date).date()
        tweets = get_tweets_by_date(username, start_date, end_date, num_tweets)

    if not tweets:
        return html.Div(
            "Error: Twitter account found, but no tweets are associated with that account.",
            style={"color": "rgb(255, 0, 0"},
        )

    texts = [row[2] for row in tweets]
    preds, judgements = dict(), dict()

    if "Toxicity" in types:
        preds["toxic"], judgements["toxic"] = pipeline.predict_toxicity_ulm_multiple(texts)
    if "Insult" in types:
        preds["insult"], judgements["insult"] = pipeline.predict_insult_multiple(texts)
    if "Obscenity" in types:
        preds["obscene"], judgements["obscene"] = pipeline.predict_obscenity_multiple(
            texts
        )
    if "Prejudice" in types:
        preds["prejudice"], judgements[
            "prejudice"
        ] = pipeline.predict_prejudice_multiple(texts)

    df = pd.DataFrame()
    df["time"] = [row[1] for row in tweets]
    df["text"] = texts

    if "Toxicity" in types:
        df["Toxicity_judgement"] = judgements["toxic"]
        df["Toxicity_pred"] = preds["toxic"]
        df["Toxicity_pred"] = df["Toxicity_pred"].map("{:.3f}".format)
    if "Insult" in types:
        df["Insult_judgement"] = judgements["insult"]
        df["Insult_pred"] = preds["insult"]
        df["Insult_pred"] = df["Insult_pred"].map("{:.3f}".format)
    if "Obscenity" in types:
        df["Obscenity_judgement"] = judgements["obscene"]
        df["Obscenity_pred"] = preds["obscene"]
        df["Obscenity_pred"] = df["Obscenity_pred"].map("{:.3f}".format)
    if "Prejudice" in types:
        df["Prejudice_judgement"] = judgements["prejudice"]
        df["Prejudice_pred"] = preds["prejudice"]
        df["Prejudice_pred"] = df["Prejudice_pred"].map("{:.3f}".format)

    table_columns = list()
    table_columns.append({"name": ["", "Time Posted"], "id": "time"})
    table_columns.append({"name": ["", "Text of Tweet"], "id": "text"})
    judgement_columns = [
        {"name": [t, "Judgement"], "id": "{}_judgement".format(t)} for t in types
    ]
    pred_columns = [
        {"name": [t, "Prediction"], "id": "{}_pred".format(t)} for t in types
    ]
    for judgement, pred in zip(judgement_columns, pred_columns):
        table_columns.append(judgement)
        table_columns.append(pred)

    table = dash_table.DataTable(
        id="table",
        columns=table_columns,
        data=df.to_dict("rows"),
        style_table={"border": "thin black solid"},
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "rgb(150,150,150)",
            "textAlign": "center",
        },
        style_cell={
            "textAlign": "left",
            "fontFamily": "optima",
            "border": "thin lightgrey solid",
            "padding": 15,
        },
        style_data={"whiteSpace": "normal"},
        css=[
            {
                "selector": ".dash-cell div.dash-cell-value",
                "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
            }
        ],
        merge_duplicate_headers=True,
        sorting=True,
        pagination_mode="fe",
        pagination_settings={"displayed_pages": 1, "current_page": 0, "page_size": 25},
    )

    y_values = dict()

    if "toxic" in preds:
        y = list()
        toxic_tweets = 0
        for total_tweets, pred in enumerate(reversed(preds["toxic"])):
            if pred > 0.4:
                toxic_tweets += 1
            y.append(toxic_tweets / (total_tweets + 1))
            total_tweets += 1
        y_values["Toxicity"] = y

    if "insult" in preds:
        y = list()
        insult_tweets = 0
        for total_tweets, pred in enumerate(reversed(preds["insult"])):
            if pred > 0.4:
                insult_tweets += 1
            y.append(insult_tweets / (total_tweets + 1))
            total_tweets += 1
        y_values["Insult"] = y

    if "obscene" in preds:
        y = list()
        obscene_tweets = 0
        for total_tweets, pred in enumerate(reversed(preds["obscene"])):
            if pred > 0.4:
                obscene_tweets += 1
            y.append(obscene_tweets / (total_tweets + 1))
            total_tweets += 1
        y_values["Obscenity"] = y

    if "prejudice" in preds:
        y = list()
        prejudice_tweets = 0
        for total_tweets, pred in enumerate(reversed(preds["obscene"])):
            if pred > 0.4:
                prejudice_tweets += 1
            y.append(prejudice_tweets / (total_tweets + 1))
            total_tweets += 1
        y_values["Prejudice"] = y

    graph = dcc.Graph(
        id="toxicity-time",
        figure={
            "data": [
                {
                    "x": [row[1] for row in reversed(tweets)],
                    "y": y_values[t],
                    "name": t,
                    "line": dict(shape="spline"),
                }
                for t in types
            ],
            "layout": {
                "title": "Ratio of Toxic Tweets Over Time",
                "xaxis": {"title": "Date and Time"},
                "yaxis": {"title": "Ratio of Toxic Tweets"},
            },
        },
    )

    over_max_tweets_message = None
    if num_tweets > 3240:
        over_max_tweets_message = html.Div(
            [
                html.P(
                    "You requested {} tweets, but Twitter limits the maximum to 3240.".format(
                        num_tweets
                    )
                )
            ],
            style={"marginBottom": "20"},
        )

    return html.Div(
        [
            html.Div(over_max_tweets_message),
            html.Div(table, style={"overflowY": "scroll", "height": "500"}),
            html.Div(graph),
        ]
    )
