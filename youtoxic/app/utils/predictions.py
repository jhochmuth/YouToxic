"""Defines functions used to make predictions of different types of toxicity.

"""


def make_predictions(text, types, pipeline):
    """Makes the predictions and classifications of specified types for a given text.

    Parameters
    ----------
    text : str
        Predictions will be made for this text.
    types : list of str
        Predictions will be made for these types of toxicity.
    pipeline : Pipeline
        The pipeline object to use to make predicitons.

    Returns
    -------
    types_order : list of str
        The types of toxicity in a specific order.
    preds : dict
        A dictionary that has lists of predictions mapped to the respective type of toxicity.
    judgements : dict
        A dictionary that has lists of judgements mapped to the respective type of toxicity.

    """
    types_order, preds, judgements = list(), dict(), dict()

    if "toxic" in types:
        preds["Toxicity"], judgements["Toxicity"] = pipeline.predict_toxicity_ulm(text)
        types_order.append("Toxicity")
    if "insult" in types:
        preds["Insult"], judgements["Insult"] = pipeline.predict_insult_ulm(text)
        types_order.append("Insult")
    if "obscene" in types:
        preds["Obscenity"], judgements["Obscenity"] = pipeline.predict_obscenity_ulm(text)
        types_order.append("Obscenity")
    if "prejudice" in types:
        preds["Prejudice"], judgements["Prejudice"] = pipeline.predict_identity_ulm(text)
        types_order.append("Prejudice")

    return types_order, preds, judgements


def make_predictions_multiple(texts, types, pipeline):
    """Makes the predictions and classifications of specified types for given texts.

    Parameters
    ----------
    texts : list of str
        Predictions will be made for these texts.
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
