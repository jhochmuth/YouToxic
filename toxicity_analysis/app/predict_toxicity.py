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


def predict_toxicity(text):
    create_model()
    torch.load('model/model.pt')
    prediction = 0
    return prediction


def predict_toxicities(texts):
    predictions = [0 for text in range(len(texts))]
    return predictions
