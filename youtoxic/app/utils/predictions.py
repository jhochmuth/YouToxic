"""Defines functions used to make predictions of different types of toxicity for a list of texts.

"""


def make_predictions_multiple(texts, types, pipeline):
    """Gets the predictions and classifications of specified types for given texts.

    Parameters
    ----------
    texts : list of str
        The texts of the tweets.
    types : list of str
        Predictions will be made for these types of toxicity.
    pipeline : Pipeline
        The pipeline object to use to make predictions.

    Returns
    -------
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.
    judgements : dict
        A dictionary that has lists of judgements mapped to the respective type of toxicity.

    """
    preds, judgements = dict(), dict()

    if "Toxicity" in types:
        preds["toxic"], judgements["toxic"] = pipeline.predict_toxicity_ulm_multiple(
            texts
        )
    if "Insult" in types:
        preds["insult"], judgements["insult"] = pipeline.predict_insult_ulm_multiple(texts)
    if "Obscenity" in types:
        preds["obscene"], judgements["obscene"] = pipeline.predict_obscenity_ulm_multiple(
            texts
        )
    if "Prejudice" in types:
        preds["prejudice"], judgements[
            "prejudice"
        ] = pipeline.predict_identity_ulm_multiple(texts)

    return preds, judgements
