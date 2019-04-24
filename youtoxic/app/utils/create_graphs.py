"""Defines functions used for creating graphs.

"""
import dash_core_components as dcc


def create_time_ratio_graph(times, types, preds):
    """Creates a Graph plotting the ratio of toxicity over time.

    Parameters
    ----------
    times : list of datetimes
        The times that the tweet/comment was created.
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.

    Returns
    -------
    dcc.Graph
        A line Graph with all data plotted.

    """
    y_values = dict()

    if "toxic" in preds:
        y = list()
        toxic_tweets = 0
        for total_tweets, pred in enumerate(preds["toxic"]):
            if pred > 0.5:
                toxic_tweets += 1
            y.append(toxic_tweets / (total_tweets + 1))
        y_values["Toxicity"] = y

    if "insult" in preds:
        y = list()
        insult_tweets = 0
        for total_tweets, pred in enumerate(preds["insult"]):
            if pred > 0.5:
                insult_tweets += 1
            y.append(insult_tweets / (total_tweets + 1))
        y_values["Insult"] = y

    if "obscene" in preds:
        y = list()
        obscene_tweets = 0
        for total_tweets, pred in enumerate(preds["obscene"]):
            if pred > 0.5:
                obscene_tweets += 1
            y.append(obscene_tweets / (total_tweets + 1))
        y_values["Obscenity"] = y

    if "prejudice" in preds:
        y = list()
        prejudice_tweets = 0
        for total_tweets, pred in enumerate(preds["prejudice"]):
            if pred > 0.5:
                prejudice_tweets += 1
            y.append(prejudice_tweets / (total_tweets + 1))
        y_values["Prejudice"] = y

    graph = dcc.Graph(
        id="ratio-time",
        figure={
            "data": [
                {
                    "x": times,
                    "y": y_values[t],
                    "name": t,
                    "line": dict(shape="spline"),
                }
                for t in types
            ],
            "layout": {
                "title": "Ratio of Toxicity Over Time",
                "xaxis": {"title": "Date and Time"},
                "yaxis": {"title": "Ratio of Toxicity"},
            },
        },
    )

    return graph


def create_time_toxicity_graph(times, types, preds):
    """Creates a Graph plotting toxicity over time.

    Parameters
    ----------
    times : list of datetimes
        The times that the tweet/comment was created.
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.

    Returns
    -------
    dcc.Graph
        A line Graph with all data plotted.

    """
    y_values = dict()
    if "toxic" in preds:
        y = list()
        total_preds = 0
        for total_tweets, pred in enumerate(preds["toxic"]):
            total_preds += pred
            y.append(total_preds / (total_tweets + 1))
        y_values["Toxicity"] = y

    if "insult" in preds:
        y = list()
        total_preds = 0
        for total_tweets, pred in enumerate(preds["insult"]):
            total_preds += pred
            y.append(total_preds / (total_tweets + 1))
        y_values["Insult"] = y

    if "obscene" in preds:
        y = list()
        total_preds = 0
        for total_tweets, pred in enumerate(preds["obscene"]):
            total_preds += pred
            y.append(total_preds / (total_tweets + 1))
        y_values["Obscenity"] = y

    if "prejudice" in preds:
        y = list()
        total_preds = 0
        for total_tweets, pred in enumerate(preds["prejudice"]):
            total_preds += pred
            y.append(total_preds / (total_tweets + 1))
        y_values["Prejudice"] = y

    graph = dcc.Graph(
        id="toxicity-time",
        figure={
            "data": [
                {
                    "x": times,
                    "y": y_values[t],
                    "name": t,
                    "line": dict(shape="spline"),
                }
                for t in types
            ],
            "layout": {
                "title": "Toxicity over Time",
                "xaxis": {"title": "Date and Time"},
                "yaxis": {"title": "Toxicity"},
            },
        },
    )

    return graph


def create_box_plot(types, preds):
    """Creates a box plot displaying the distribution for each type of toxicity.

    Parameters
    ----------
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.

    Returns
    -------
    dcc.Graph
        The box plot with all distributions displayed.

    """
    type_ids = list()

    if "Toxicity" in types:
        type_ids.append("toxic")
    if "Insult" in types:
        type_ids.append("insult")
    if "Obscenity" in types:
        type_ids.append("obscene")
    if "Identity hate" in types:
        type_ids.append("prejudice")

    data = []

    for type_id, type_name in zip(type_ids, types):
        trace = {
            "type": 'box',
            "x": type_id,
            "y": preds[type_id],
            "name": type_name,
            "box": {
                "visible": True
            },
            "meanline": {
                "visible": True
            }
        }
        data.append(trace)

    graph = dcc.Graph(
        id='toxicity-distribution',
        figure={
            "data": data,
            "layout": {
                "title": "Toxicity Distributions",
                "yaxis": {
                    "zeroline": False,
                    "title": "Prediction",
                }
            }
        }
    )

    return graph


def create_violin_plot(types, preds):
    """Creates a violin plot displaying the distribution for each type of toxicity.

    Parameters
    ----------
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.

    Returns
    -------
    dcc.Graph
        The violin plot with all distributions displayed.

    """
    type_ids = list()

    if "Toxicity" in types:
        type_ids.append("toxic")
    if "Insult" in types:
        type_ids.append("insult")
    if "Obscenity" in types:
        type_ids.append("obscene")
    if "Identity hate" in types:
        type_ids.append("prejudice")

    data = []

    for type_id, type_name in zip(type_ids, types):
        trace = {
            "type": 'violin',
            "x": type_id,
            "y": preds[type_id],
            "name": type_name,
            "box": {
                "visible": True
            },
            "meanline": {
                "visible": True
            }
        }
        data.append(trace)

    graph = dcc.Graph(
        id='toxicity-distribution',
        figure={
            "data": data,
            "layout": {
                "title": "Toxicity Distributions",
                "yaxis": {
                    "zeroline": False,
                    "title": "Prediction",
                }
            }
        }
    )

    return graph
