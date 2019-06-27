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

## Usage
Visit the IP address specified above.

If you are trying to run the application locally, you need to provide environment variables that contain credentials for the twitter API credentials and youtube API. Tweets and youtube comments cannot be collected unless you provide these. Predictions on text entered manually are still possible even without providing the credentials.

These are the necessary environment variables:
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, YOUTUBE_KEY

The first four variables are all for the twitter API. 

## Documentation
YouToxic uses [Sphinx](http://www.sphinx-doc.org/en/master/) to build the documentation.
To build
```
cd docs
make html
```
