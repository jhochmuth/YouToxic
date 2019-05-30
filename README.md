# YouToxic
A Python web application that predicts the toxicity of text using Deep Learning.
You can access the app at the following IP address: 104.154.107.241.

## Specifics
The framework of the app was built primarily with [Dash by Plotly](https://dash.plot.ly).

The predictions are generated with ULMFiT models trained on the dataset provided for the
Jigsaw Toxic Comment Classification Kaggle competition.
You can find the dataset [here](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data).

Currently, predictions can be made for 4 types of toxicity:
general toxicity, insults, obscenity, and prejudice/identity hate.

## Documentation
YouToxic uses [Sphinx](http://www.sphinx-doc.org/en/master/) to build the documentation.
To build
```
cd docs
make html
```