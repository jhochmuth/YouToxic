"""Contains implementation of the functions used for loading the mappings and models.

"""
import collections
import pickle
from pathlib import Path

import numpy as np

import torch

from youtoxic.app.utils.lm_rnn import get_rnn_classifier


def load_mappings(mappings_filename):
    """Loads the vocabulary mappings.

    Parameters
    ----------
    mappings_filename: str
        The file containing the vocabulary mappings.

    Returns
    -------
    defaultdict
        The vocabulary mappings contained within the specified file.

    """
    itos = pickle.load(Path(mappings_filename).open("rb"))
    stoi = collections.defaultdict(
        lambda: 0, {str(v): int(k) for k, v in enumerate(itos)}
    )
    return stoi


def load_model(vocab_size, classifier_filename):
    """Loads a trained ULMFiT model.

    Parameters
    ----------
    vocab_size: int
        The number of unique vocabulary tokens.
    classifier_filename: str
        The file containing the trained classifier

    Returns
    -------
    SequentialRNN
        The trained classifer model.

    """
    bptt, em_sz, nh, nl = 70, 400, 1150, 3
    dps = np.array([0.4, 0.5, 0.05, 0.3, 0.4]) * 0.5
    vs = vocab_size

    model = get_rnn_classifier(
        bptt,
        20 * bptt,
        2,
        vs,
        emb_sz=em_sz,
        n_hid=nh,
        n_layers=nl,
        pad_token=1,
        layers=[em_sz * 3, 50, 2],
        drops=[dps[4], 0.1],
        dropouti=dps[0],
        wdrop=dps[1],
        dropoute=dps[2],
        dropouth=dps[3],
    )

    sd = torch.load(classifier_filename, map_location=lambda storage, loc: storage)
    names = set(model.state_dict().keys())
    for n in list(sd.keys()):
        if n not in names and n + "_raw" in names:
            if n + "_raw" not in sd:
                sd[n + "_raw"] = sd[n]
            del sd[n]
    model.load_state_dict(sd)

    model.reset()
    model.eval()
    return model
