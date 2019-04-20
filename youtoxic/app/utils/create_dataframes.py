"""Defines functions used for creating dataframes.

"""
import pandas as pd


def create_tweets_dataframe(tweets, types, preds, judgements):
    """Creates a DataFrame from tweet data.

    Parameters
    ----------
    tweets : list of lists
        The list of tweets.
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

    df["time"] = [row[1] for row in tweets]
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
