"""Contains implementation of the Pipeline object."""

import pickle

from keras_preprocessing.sequence import pad_sequences

import numpy as np

import torch

from youtoxic.app.utils.path import get_abs_path
from youtoxic.app.utils.neural_net import NeuralNet


class Pipeline:
    """This object loads all models and makes the actual predictions."""

    def __init__(self):
        """Initializes pipeline object by loading models and tokenizer."""
        import os
        import youtoxic

        p = os.path.dirname(youtoxic.__file__)
        #self.toxicity_model = torch.load(get_abs_path("app/models/toxicity_model.pt"))
        #self.identity_model = torch.load(get_abs_path("app/models/identity_model.pt"))
        #self.obscenity_model = torch.load(get_abs_path("app/models/obscenity_model.pt"))
        #self.insult_model = torch.load(get_abs_path("app/models/insult_model.pt"))
        self.toxicity_model = NeuralNet()
        self.toxicity_model.load_state_dict(torch.load("youtoxic/app/models/identity_model_state.pt"))
        self.identity_model, self.obscenity_model, self.insult_model = self.toxicity_model, self.toxicity_model, self.toxicity_model
        self.toxicity_model.eval()
        self.identity_model.eval()
        self.obscenity_model.eval()
        self.insult_model.eval()
        self.threshold = 0.4

        with open(get_abs_path("app/utils/tokenizer.pickle"), "rb") as handle:
            self.tokenizer = pickle.load(handle)

    @staticmethod
    def get_features(texts):
        """Calculates extra features for specified texts.

        Notes
        -----
        Models were trained when caps_vs_length feature was always set to 0.

        Parameters
        ----------
        texts: List
            A list of strings, each of which represents one individual text.

        Returns
        -------
        List
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

    @staticmethod
    def standardize_features(features):
        """Standardizes features using a pre-fit Standard Scalar object.

        Parameters
        ----------
        features: List
            A list containing the features to standardize.

        Returns
        -------
        List
            A list containing the standardized features.

        """
        with open(get_abs_path("app/utils/scalar.pickle"), "rb") as handle:
            ss = pickle.load(handle)
        features = ss.transform(features)
        return features

    @staticmethod
    def sigmoid(x):
        """Defines the sigmoid function."""
        return 1 / (1 + np.exp(-x))

    def predict_insult(self, text):
        """Predicts if a text is an insult.

        Parameters
        ----------
        text: str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.

        str
            'Insult' if prediction > threshold, 'Not an insult' otherwise.

        """
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.insult_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = "Insult" if result[0][0] > self.threshold else "Not an insult"
        return round(result[0][0], 3), classification

    def predict_insult_multiple(self, texts):
        """Predicts if each text in a list is an insult.

        Parameters
        ----------
        texts: List
            A list of texts to make predictions for.

        Returns
        -------
        preds: List
            Contains the numeric prediction for each text.

        classifications: List
            For each text, contains 'Insult' if prediction > threshold, 'Not an insult' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.insult_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = [
            "Insult" if pred > self.threshold else "Not an insult" for pred in preds
        ]
        return preds, classifications

    def predict_obscenity(self, text):
        """Predicts if a text contains obscenity.

        Parameters
        ----------
        text: str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.

        str
            'Obscene' if prediction > threshold, 'Not obscene' otherwise.

        """
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.obscenity_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = "Obscene" if result[0][0] > self.threshold else "Not obscene"
        return round(result[0][0], 3), classification

    def predict_obscenity_multiple(self, texts):
        """Predicts if each text in a list contains obscenity.

        Parameters
        ----------
        texts: List
            A list of texts to make predictions for.

        Returns
        -------
        preds: List
            Contains the numeric prediction for each text.

        classifications: List
            For each text, contains 'Obscene' if prediction > threshold, 'Not obscene' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.obscenity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = [
            "Obscene" if pred > self.threshold else "Not obscene" for pred in preds
        ]
        return preds, classifications

    def predict_prejudice(self, text):
        """Predicts if a text contains prejudice/identity hate.

        Parameters
        ----------
        text: str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.

        str
            'Prejudice' if prediction > threshold, 'Not prejudice' otherwise.

        """
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.identity_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = (
            "Prejudice" if result[0][0] > self.threshold else "Not prejudice"
        )
        return round(result[0][0], 3), classification

    def predict_prejudice_multiple(self, texts):
        """Predicts if each text in a list contains prejudice/identity hate.

        Parameters
        ----------
        texts: List
            A list of texts to make predictions for.

        Returns
        -------
        preds: List
            Contains the numeric prediction for each text.

        classifications: List
            For each text, contains 'Prejudice' if prediction > threshold, 'Not prejudice' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.identity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = [
            "Prejudice" if pred > self.threshold else "Not prejudice" for pred in preds
        ]
        return preds, classifications

    def predict_toxicity(self, text):
        """Predicts if a text contains general toxicity.

        Parameters
        ----------
        text: str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.

        str
            'Toxic' if prediction > threshold, 'Not toxic' otherwise.

        """
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.toxicity_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = "Toxic" if result[0][0] > self.threshold else "Not toxic"
        return round(result[0][0], 3), classification

    def predict_toxicity_multiple(self, texts):
        """Predicts if each text in a list contains general toxicity.

        Parameters
        ----------
        texts: List
            A list of texts to make predictions for.

        Returns
        -------
        preds: List
            Contains the numeric prediction for each text.

        classifications: List
            For each text, contains 'Toxic' if prediction > threshold, 'Not toxic' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.toxicity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = [
            "Toxic" if pred > self.threshold else "Not toxic" for pred in preds
        ]
        return preds, classifications
