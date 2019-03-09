from keras_preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import torch


class Pipeline:
    toxicity_model = None
    identity_model = None
    tokenizer = None
    embeddings = None

    def __init__(self):
        self.toxicity_model = torch.load('youtoxic/app/models/toxicity_model.pt')
        self.identity_model = torch.load('youtoxic/app/models/identity_model.pt')
        self.toxicity_model.eval()
        self.identity_model.eval()

        with open('youtoxic/app/utils/tokenizer.pickle', 'rb') as handle:
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
        with open('youtoxic/app/utils/scalar.pickle', 'rb') as handle:
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
        classification = 'Identity hate' if result[0][0] > .4 else 'Not identity hate'
        return result[0][0], classification

    def predict_identity_hate_multiple(self, texts):
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.identity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = ['Identity hate' if pred > .4 else 'Not identity hate' for pred in preds]
        return preds, classifications

    def predict_toxicity(self, text):
        x = self.tokenizer.texts_to_sequences([text])
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features([text])
        features = self.standardize_features(features)

        pred = self.toxicity_model([x, features]).detach()
        result = self.sigmoid(pred.numpy())
        classification = 'Toxic' if result[0][0] > .4 else 'Not toxic'
        return result[0][0], classification

    def predict_toxicity_multiple(self, texts):
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = self.get_features(texts)
        features = self.standardize_features(features)

        preds = self.toxicity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in self.sigmoid(preds.numpy())]
        classifications = ['Toxic' if pred > .4 else 'Not toxic' for pred in preds]
        return preds, classifications
