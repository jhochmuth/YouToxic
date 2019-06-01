"""Defines functions used for creating dataframes.

"""
import pandas as pd


def create_text_df(types, preds, judgements):
    """Creates a DataTable from text data.

    Parameters
    ----------
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.
    judgements : dict
        A dictionary that has lists of judgements mapped to the respective type of toxicity.

    Returns
    -------
    DataFrame
        A DataFrame containing information about the text.

    """
    df = pd.DataFrame()
    df["type"] = types
    df["judgement"] = df["type"].map(judgements)
    df["pred"] = df["type"].map(preds)
    df["pred"] = df["pred"].map("{:.3f}".format)
    return df


def create_tweets_df(tweets, types, preds, judgements):
    """Creates a DataFrame from tweet data.

    Parameters
    ----------
    tweets : list of lists
        Contains the tweets. Each item in the list is a separate list with all information about the tweet.
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.
    judgements : dict
        A dictionary that has lists of judgements mapped to the respective type of toxicity.

    Returns
    -------
    DataFrame
        A DataFrame containing information about the tweets.

    """
    df = pd.DataFrame()

    df["time"] = [row[1].astimezone() for row in tweets]
    df["text"] = [row[2] for row in tweets]

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

    return df


def create_youtube_df(comments, authors, times, types, preds, judgements):
    """Creates a DataFrame from youtube data.

    Parameters
    ----------
    comments : list of str
        A list containing the text of each comment.
    authors : list of str
        A list containing the author of each comment.
    times : list of datetime
        A list containing the date and time when each comment was posted.
    types : list of str
        The types of toxicity.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.
    judgements : dict
        A dictionary that has lists of judgements mapped to the respective type of toxicity.

    Returns
    -------
    DataFrame
        A DataFrame containing information about the tweets.

    """
    df = pd.DataFrame()

    df["text"] = comments
    df["author"] = authors
    df["time"] = times

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

    return df
