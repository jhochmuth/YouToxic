"""For predicting the toxicities of tweets of a specified Twitter user.

"""
import dash_html_components as html

from dateutil import parser

from youtoxic.app.services.tweet_dumper import (
    get_tweets,
    get_tweets_by_date,
    validate_username,
)
from youtoxic.app.utils.create_dataframes import create_tweets_df
from youtoxic.app.utils.create_graphs import create_average_toxicity_graph, create_violin_plot
from youtoxic.app.utils.create_tables import create_tweets_table
from youtoxic.app.utils.predictions import make_predictions_multiple
from youtoxic.app.utils.preprocessing import preprocess_texts


def get_tweet_predictions(
    username, num_tweets, types, limit_date, start_date, end_date, pipeline
):
    """Collects tweets, analyzes them, and creates a table and a line graph.

    Parameters
    ----------
    username : str
        Tweets will be collected from this user.
    num_tweets : int
        The maximum number of tweets to analyze.
    types : list of str
        Predictions will be made for these types of toxicity
    limit_date : str
        Whether to get tweets between a certain date range ('date') or the most recent tweets ('all').
    start_date : Datetime
        Minimum date for date-limited collection. Only matters if limit_date == 'date'.
    end_date : Datetime
        Maximum date for date-limited collection. Only matters if limit_date == 'date'.
    pipeline : Pipeline
        The pipeline object used to make predictions.

    Returns
    -------
    html.Div
        The html layout for the subsection of the page that contains results.

    """
    if username.lower() == "realdonaldtrump":
        return html.Div(
            "Is that really necessary? It is obvious that those tweets contain nothing of value.",
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
            "Error: Twitter account found, but no tweets are associated with that account within the specified dates.",
            style={"color": "rgb(255, 0, 0"},
        )

    times = list(reversed([row[1].astimezone() for row in tweets]))
    texts = list(reversed([row[2] for row in tweets]))
    texts = preprocess_texts(texts)
    preds, judgements = make_predictions_multiple(texts, types, pipeline)
    df = create_tweets_df(tweets, types, preds, judgements)

    table = create_tweets_table(df, types)
    graph = create_average_toxicity_graph(times, types, preds)
    violin_plot = create_violin_plot(types, preds)

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
            style={"marginBottom": 20},
            className="row",
        )

    return html.Div(
        [
            html.Div(over_max_tweets_message),
            html.Div(children=[
                html.Div(table, className="six columns", style={"overflow": "scroll", "height": 922}),
                html.Div(graph, className="six columns", style={"marginBottom": 20}),
                html.Div(violin_plot, className="six columns"),
            ],
                className="row",
                style={"marginBottom": 20},
            )
        ],
    )
