"""Contains implementation of functions used to preprocess the text of tweets before passing them to models.

"""


def preprocess_text(text):
    """Preprocesses a single tweet.

    Parameters
    ----------
    text : str
        The tweet to preprocess.

    Returns
    -------
    str
        The preprocessed text.

    """
    words = text.split()
    preprocessed = list()
    for word in words:
        if '@' not in word and 'http' not in word:
            preprocessed.append(word)
    return ' '.join(preprocessed)


def preprocess_texts(texts):
    """Preprocesses multiple tweets.

    Parameters
    ----------
    texts : List
        The tweets to preprocess.

    Returns
    -------
    List
        The preprocessed texts.

    """
    return [preprocess_text(text) for text in texts]
