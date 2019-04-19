"""Contains implementation of function used to preprocess text of tweets."""


def preprocess_text(text):
    words = text.split()
    preprocessed = list()
    for word in words:
        if '@' not in word and 'http' not in word:
            preprocessed.append(word)
    return ' '.join(preprocessed)


def preprocess_texts(texts):
    return [preprocess_text(text) for text in texts]
