"""Contains implementation of the Pipeline object.

"""
from fastai.text.transform import Tokenizer

import numpy as np

import torch
from torch.autograd.variable import Variable

from youtoxic.app.utils.functions import softmax
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

    def __init__(self, threshold=0.5):
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
            return 0
        texts = [text]
        tok = self.tokenizer.process_all(texts)
        encoded = [mappings[p] for p in tok[0]]
        ary = np.reshape(np.array(encoded), (-1, 1))
        tensor = torch.from_numpy(ary)
        variable = Variable(tensor)

        predictions = model(variable)
        numpy_preds = predictions[0].data.numpy()
        return softmax(numpy_preds[0])[0][1]

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
        pred = self.predict_text_ulm(self.ulm_toxicity_model, self.toxicity_mappings, text)
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
        pred = self.predict_text_ulm(self.ulm_insult_model, self.insult_mappings, text)
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
        pred = self.predict_text_ulm(self.ulm_obscenity_model, self.obscenity_mappings, text)
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
        pred = self.predict_text_ulm(self.ulm_identity_model, self.identity_mappings, text)
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
