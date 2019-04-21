"""Contains implementation of the Pipeline object.

"""
from fastai.text.transform import Tokenizer

from keras_preprocessing.sequence import pad_sequences

import numpy as np

import torch
from torch.autograd.variable import Variable

from youtoxic.app.utils.feature_engineering import get_features, standardize_features
from youtoxic.app.utils.functions import sigmoid, softmax
from youtoxic.app.utils.load_files import load_mappings, load_model


class Pipeline:
    """This object loads all models and is used to make predictions.

    Attributes
    ----------
    threshold : float
        The value to use when making a judgement on toxicity.
    toxicity_mappings : defaultdict
        The vocabulary mappings used for the toxicity model.
    ulm_toxicity_model : SequentialRNN
        The trained model for toxicity analysis.
    insult_mappings : defaultdict
        The vocabulary mappings used for the insult model.
    ulm_insult_model : SequentialRNN
        The trained model for insult analysis.
    obscenity_mappings : defaultdict
        The vocabulary mappings used for the obscenity model.
    ulm_obscenity_model : SequentialRNN
        The trained model for obscenity analysis.
    identity_mappings : defaultdict
        The vocabulary mappings used for the identity hate model.
    ulm_identity_model : SequentialRNN
        The trained model for identity hate analysis.

    """

    def __init__(self, threshold=0.4):
        """Initializes pipeline object by loading models and tokenizer.

        Parameters
        ----------
        threshold : float
            The value to use when making a judgement on toxicity.

        """
        self.threshold = threshold
        self.tokenizer = Tokenizer()

        self.toxicity_mappings = load_mappings("youtoxic/app/models/toxicity_mappings.pkl")
        self.ulm_toxicity_model = load_model(
            len(self.toxicity_mappings), "youtoxic/app/models/toxicity_model.h5"
        )

        self.insult_mappings = load_mappings("youtoxic/app/models/insult_mappings.pkl")
        self.ulm_insult_model = load_model(len(self.insult_mappings), "youtoxic/app/models/insult_model.h5")

        self.obscenity_mappings = load_mappings("youtoxic/app/models/obscenity_mappings.pkl")
        self.ulm_obscenity_model = load_model(len(self.obscenity_mappings), "youtoxic/app/models/obscenity_model.h5")

        self.identity_mappings = load_mappings("youtoxic/app/models/identity_mappings.pkl")
        self.ulm_identity_model = load_model(len(self.identity_mappings), "youtoxic/app/models/identity_model.h5")

        # The following code initializes the old RNN models.
        """
        self.toxicity_model = NeuralNet()
        self.identity_model = NeuralNet()
        self.obscenity_model = NeuralNet()
        self.insult_model = NeuralNet()
        
        self.toxicity_model.load_state_dict(
            torch.load("youtoxic/app/models/toxicity_model_state.pt")
        )
        self.identity_model.load_state_dict(
            torch.load("youtoxic/app/models/identity_model_state.pt")
        )
        self.obscenity_model.load_state_dict(
            torch.load("youtoxic/app/models/obscenity_model_state.pt")
        )
        self.insult_model.load_state_dict(
            torch.load("youtoxic/app/models/insult_model_state.pt")
        )

        self.toxicity_model.eval()
        self.identity_model.eval()
        self.obscenity_model.eval()
        self.insult_model.eval()
        
        with open("youtoxic/app/utils/tokenizer.pickle", "rb") as handle:
            self.tokenizer = pickle.load(handle)
        """

    def predict_insult(self, text):
        """Predicts if a text is an insult.

        Parameters
        ----------
        text : str
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

        features = get_features([text])
        features = standardize_features(features)

        pred = self.insult_model([x, features]).detach()
        result = sigmoid(pred.numpy())
        classification = "Insult" if result[0][0] > self.threshold else "Not an insult"
        return round(result[0][0], 3), classification

    def predict_insult_multiple(self, texts):
        """Predicts if each text in a list is an insult.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        list of float
            Contains the numeric prediction for each text.
        list of str
            For each text, contains 'Insult' if prediction > threshold, 'Not an insult' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = get_features(texts)
        features = standardize_features(features)

        preds = self.insult_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in sigmoid(preds.numpy())]
        classifications = [
            "Insult" if pred > self.threshold else "Not an insult" for pred in preds
        ]
        return preds, classifications

    def predict_obscenity(self, text):
        """Predicts if a text contains obscenity.

        Parameters
        ----------
        text : str
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

        features = get_features([text])
        features = standardize_features(features)

        pred = self.obscenity_model([x, features]).detach()
        result = sigmoid(pred.numpy())
        classification = "Obscene" if result[0][0] > self.threshold else "Not obscene"
        return round(result[0][0], 3), classification

    def predict_obscenity_multiple(self, texts):
        """Predicts if each text in a list contains obscenity.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        list of float
            Contains the numeric prediction for each text.
        list of str
            For each text, contains 'Obscene' if prediction > threshold, 'Not obscene' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = get_features(texts)
        features = standardize_features(features)

        preds = self.obscenity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in sigmoid(preds.numpy())]
        classifications = [
            "Obscene" if pred > self.threshold else "Not obscene" for pred in preds
        ]
        return preds, classifications

    def predict_prejudice(self, text):
        """Predicts if a text contains prejudice/identity hate.

        Parameters
        ----------
        text : str
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

        features = get_features([text])
        features = standardize_features(features)

        pred = self.identity_model([x, features]).detach()
        result = sigmoid(pred.numpy())
        classification = (
            "Prejudice" if result[0][0] > self.threshold else "Not prejudice"
        )
        return round(result[0][0], 3), classification

    def predict_prejudice_multiple(self, texts):
        """Predicts if each text in a list contains prejudice/identity hate.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        list of float
            Contains the numeric prediction for each text.
        list of str
            For each text, contains 'Prejudice' if prediction > threshold, 'Not prejudice' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = get_features(texts)
        features = standardize_features(features)

        preds = self.identity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in sigmoid(preds.numpy())]
        classifications = [
            "Prejudice" if pred > self.threshold else "Not prejudice" for pred in preds
        ]
        return preds, classifications

    def predict_toxicity(self, text):
        """Predicts if a text contains general toxicity.

        Parameters
        ----------
        text : str
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

        features = get_features([text])
        features = standardize_features(features)

        pred = self.toxicity_model([x, features]).detach()
        result = sigmoid(pred.numpy())
        classification = "Toxic" if result[0][0] > self.threshold else "Not toxic"
        return round(result[0][0], 3), classification

    def predict_toxicity_multiple(self, texts):
        """Predicts if each text in a list contains general toxicity.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        preds : list of float
            Contains the numeric prediction for each text.
        classifications: list of float
            For each text, contains 'Toxic' if prediction > threshold, 'Not toxic' otherwise.

        """
        x = self.tokenizer.texts_to_sequences(texts)
        x = pad_sequences(x, maxlen=70)
        x = torch.tensor(x, dtype=torch.long)

        features = get_features(texts)
        features = standardize_features(features)

        preds = self.toxicity_model([x, features]).detach()
        preds = [round(pred[0], 3) for pred in sigmoid(preds.numpy())]
        classifications = [
            "Toxic" if pred > self.threshold else "Not toxic" for pred in preds
        ]
        return preds, classifications

    def predict_text_ulm(self, model, mappings, text):
        """Makes predictions using the given ULMFiT model.

        Parameters
        ----------
        model : SequentialRNN
            The ULMFiT model to use for making predictions.
        mappings : defaultdict
            The corresponding vocabulary mappings for the model.
        text : str
            The text to analyze.

        Returns
        -------
        float
            The prediction.

        """
        if len(text.split()) == 0:
            return [1, 0]
        texts = [text]
        tok = self.tokenizer.process_all(texts)
        encoded = [mappings[p] for p in tok[0]]

        ary = np.reshape(np.array(encoded), (-1, 1))
        tensor = torch.from_numpy(ary)
        variable = Variable(tensor)

        predictions = model(variable)
        numpy_preds = predictions[0].data.numpy()
        return softmax(numpy_preds[0])[0]

    def predict_toxicity_ulm(self, text):
        """Predicts if a text contains general toxicity using a ULMFiT model.

        Parameters
        ----------
        text : str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.
        str
            'Toxic' if prediction > threshold, 'Not toxic' otherwise.

        """
        pred = self.predict_text_ulm(self.ulm_toxicity_model, self.toxicity_mappings, text)[1]
        classification = "Toxic" if pred > self.threshold else "Not toxic"
        return pred, classification

    def predict_toxicity_ulm_multiple(self, texts):
        """Predicts if each text in a list contains general toxicity using a ULMFiT model.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        list of float
            Contains the numeric prediction for each text.
        list of str
            For each text, contains 'Toxic' if prediction > threshold, 'Not toxic' otherwise.

        """
        preds, classifications = [None] * len(texts), [None] * len(texts)
        for i, text in enumerate(texts):
            preds[i], classifications[i] = self.predict_toxicity_ulm(text)
        return preds, classifications

    def predict_insult_ulm(self, text):
        """Predicts if a text contains an insult using a ULMFiT model.

        Parameters
        ----------
        text : str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.
        str
            'Insult' if prediction > threshold, 'Not an insult' otherwise.

        """
        pred = self.predict_text_ulm(self.ulm_insult_model, self.insult_mappings, text)[1]
        classification = "Insult" if pred > self.threshold else "Not an insult"
        return pred, classification

    def predict_insult_ulm_multiple(self, texts):
        """Predicts if each text in a list contains an insult using a ULMFiT model.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        list of float
            Contains the numeric prediction for each text.
        list of str
            For each text, contains 'Insult' if prediction > threshold, 'Not an insult' otherwise.

        """
        preds, classifications = [None] * len(texts), [None] * len(texts)
        for i, text in enumerate(texts):
            preds[i], classifications[i] = self.predict_insult_ulm(text)
        return preds, classifications

    def predict_obscenity_ulm(self, text):
        """Predicts if a text contains obscenity using a ULMFiT model.

        Parameters
        ----------
        text : str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.
        str
            'Obscene' if prediction > threshold, 'Not obscene' otherwise.

        """
        pred = self.predict_text_ulm(self.ulm_obscenity_model, self.obscenity_mappings, text)[1]
        classification = "Obscene" if pred > self.threshold else "Not obscene"
        return pred, classification

    def predict_obscenity_ulm_multiple(self, texts):
        """Predicts if each text in a list contains obscenity using a ULMFiT model.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        list of float
            Contains the numeric prediction for each text.
        list of str
            For each text, contains 'Obscene' if prediction > threshold, 'Not obscene' otherwise.

        """
        preds, classifications = [None] * len(texts), [None] * len(texts)
        for i, text in enumerate(texts):
            preds[i], classifications[i] = self.predict_obscenity_ulm(text)
        return preds, classifications

    def predict_identity_ulm(self, text):
        """Predicts if a text contains identity hate using a ULMFiT model.

        Parameters
        ----------
        text : str
            The text to make a prediction for.

        Returns
        -------
        float
            The numeric prediction.
        str
            'Identity hate' if prediction > threshold, 'Not identity hate' otherwise.

        """
        pred = self.predict_text_ulm(self.ulm_identity_model, self.identity_mappings, text)[1]
        classification = "Identity hate" if pred > self.threshold else "Not identity hate"
        return pred, classification

    def predict_identity_ulm_multiple(self, texts):
        """Predicts if each text in a list contains identity hate using a ULMFiT model.

        Parameters
        ----------
        texts : list of str
            A list of texts to make predictions for.

        Returns
        -------
        list of float
            Contains the numeric prediction for each text.
        list of str
            For each text, contains 'Identity hate' if prediction > threshold, 'Not identity hate' otherwise.

        """
        preds, classifications = [None] * len(texts), [None] * len(texts)
        for i, text in enumerate(texts):
            preds[i], classifications[i] = self.predict_identity_ulm(text)
        return preds, classifications
