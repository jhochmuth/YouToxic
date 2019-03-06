from keras_preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import torch


def create_model():
    files = list()
    files.append('model/model_1.pt')
    files.append('model/model_2.pt')
    files.append('model/model_3.pt')
    files.append('model/model_4.pt')
    files.append('model/model_5.pt')

    with open('model/model.pt', 'wb') as outfile:
        for file in files:
            with open(file, 'rb') as infile:
                outfile.write(infile.read())


def create_embeddings():
    files = list()
    files.append('embedding_matrix/embedding_matrix_1.npy')
    files.append('embedding_matrix/embedding_matrix_2.npy')
    files.append('embedding_matrix/embedding_matrix_3.npy')
    files.append('embedding_matrix/embedding_matrix_4.npy')
    files.append('embedding_matrix/embedding_matrix_5.npy')
    files.append('embedding_matrix/embedding_matrix_6.npy')
    files.append('embedding_matrix/embedding_matrix_7.npy')
    files.append('embedding_matrix/embedding_matrix_8.npy')
    files.append('embedding_matrix/embedding_matrix_9.npy')
    files.append('embedding_matrix/embedding_matrix_10.npy')

    with open('embedding_matrix/embedding_matrix.npy', 'wb') as outfile:
        for file in files:
            with open(file, 'rb') as infile:
                outfile.write(infile.read())


def create_tokenizer():
    with open('tokenizer.pkl', 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def predict_toxicity(text):
    try:
        model = torch.load('model/model.pt')
    except FileNotFoundError:
        create_model()
        model = torch.load('model/model.pt')

    model.eval()

    tokenizer = create_tokenizer()
    texts = list()
    for _ in range(2):
        texts.append(text)
    x = tokenizer.texts_to_sequences(texts)
    x = pad_sequences(x, maxlen=70)
    x = torch.tensor([x], dtype=torch.long)

    caps_vs_length = .2
    words_vs_unique = .5
    features = list()
    for _ in range(2):
        features.append([caps_vs_length, words_vs_unique])
    pred = model([x, features]).detach()
    result = sigmoid(pred.numpy())
    return result[0]


def predict_toxicities(texts):
    predictions = [0 for text in range(len(texts))]
    return predictions
