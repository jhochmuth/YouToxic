"""Defines functions used for creating graphs.

"""
import dash_core_components as dcc


def create_tweets_graph(tweets, types, preds):
    """Creates a Graph displaying information about the given tweets.

    Parameters
    ----------
    tweets : list of lists
        The list of tweets.
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.

    Returns
    -------
    Graph
        A line Graph with all data plotted.

    """
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
        for total_tweets, pred in enumerate(reversed(preds["prejudice"])):
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

    return graph
