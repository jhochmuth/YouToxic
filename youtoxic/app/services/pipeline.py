import pickle

from keras_preprocessing.sequence import pad_sequences

import numpy as np

import torch


class Pipeline:
    toxicity_model = None
    identity_model = None
    tokenizer = None
    embeddings = None

    def __init__(self):
        self.toxicity_model = torch.load("youtoxic/app/models/toxicity_model.pt")
        self.identity_model = torch.load("youtoxic/app/models/identity_model.pt")
        self.obscenity_model = torch.load("youtoxic/app/models/obscenity_model.pt")
        self.insult_model = torch.load("youtoxic/app/models/insult_model.pt")
        self.toxicity_model.eval()
        self.identity_model.eval()
        self.obscenity_model.eval()
        self.insult_model.eval()

        with open("youtoxic/app/utils/tokenizer.pickle", "rb") as handle:
            self.tokenizer = pickle.load(handle)

    # Note: models were trained when caps_vs_length feature was always 0.
    @staticmethod
    def get_features(texts):
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
        with open("youtoxic/app/utils/scalar.pickle", "rb") as handle:
            ss = pickle.load(handle)
        features = ss.transform(features)
        return features

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def predict_identity_hate(self, text):
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.identity_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = "Identity hate" if result[0][0] > 0.4 else "Not identity hate"
        return round(result[0][0], 3), classification

    def predict_identity_hate_multiple(self, texts):
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.identity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = ["Identity hate" if pred > 0.4 else "Not identity hate" for pred in preds]
        return preds, classifications

    def predict_insult(self, text):
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.insult_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = "Insult" if result[0][0] > 0.4 else "Not an insult"
        return round(result[0][0], 3), classification

    def predict_insult_multiple(self, texts):
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.insult_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = ["Insult" if pred > 0.4 else "Not an insult" for pred in preds]
        return preds, classifications

    def predict_obscenity(self, text):
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.obscenity_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = "Obscene" if result[0][0] > 0.4 else "Not obscene"
        return round(result[0][0], 3), classification

    def predict_obscenity_multiple(self, texts):
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.obscenity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = ["Obscene" if pred > 0.4 else "Not obscene" for pred in preds]
        return preds, classifications

    def predict_toxicity(self, text):
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.toxicity_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = "Toxic" if result[0][0] > 0.4 else "Not toxic"
        return round(result[0][0], 3), classification

    def predict_toxicity_multiple(self, texts):
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.toxicity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = ["Toxic" if pred > 0.4 else "Not toxic" for pred in preds]
        return preds, classifications
