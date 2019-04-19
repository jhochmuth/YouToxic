"""Contains implementation of functions used for feature engineering.

"""
import pickle


def get_features(texts):
    """Calculates extra features for specified texts.

    Notes
    -----
    Models were trained when caps_vs_length feature was always set to 0.

    Parameters
    ----------
    texts: list of str
        The texts from which features are created.

    Returns
    -------
    list of lists
        Each value of the list contains a value representing each feature: caps_vs_length and words_vs_unique.

    """
    features = list()
    for text in texts:
        text = text.lower()
        length = len(text)
        capitals = sum(1 for c in text if c.isupper())
        caps_vs_length = capitals / length
        num_words = len(text.split())
        num_unique_words = len(set(text.lower().split()))
        words_vs_unique = num_unique_words / num_words
        features.append([caps_vs_length, words_vs_unique])
    return features


def standardize_features(features):
    """Standardizes features using a pre-fit Standard Scalar object.

    Parameters
    ----------
    features: list of lists
        The features to standardize.

    Returns
    -------
    list of lists
        Contains the standardized features.

    """
    with open("youtoxic/app/utils/scalar.pickle", "rb") as handle:
        ss = pickle.load(handle)
    features = ss.transform(features)
    return features
