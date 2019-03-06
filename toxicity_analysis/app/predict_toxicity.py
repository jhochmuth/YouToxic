#from keras.preprocessing.sequence import pad_sequences
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


def predict_toxicity(text):
    try:
        model = torch.load('model/model.pt')
    except FileNotFoundError:
        create_model()
        model = torch.load('model/model.pt')

    try:
        embedding_matrix = np.load('embedding_matrix/embedding_matrix.npy')
    except FileNotFoundError:
        create_embeddings()
        embedding_matrix = np.load('embedding_matrix/embedding_matrix.npy')

    model.eval()

    tokenizer = create_tokenizer()
    x = tokenizer.texts_to_sequences(text)
    x = torch.tensor(x)
    caps_vs_length = 0
    words_vs_unique = 0
    print(model(x))
    return 0


def predict_toxicities(texts):
    predictions = [0 for text in range(len(texts))]
    return predictions
