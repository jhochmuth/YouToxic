# YouToxic
A Python web application that predicts the toxicity of text using Deep Learning.
App is no longer deployed on a cluster.

## Demo
![](https://drive.google.com/file/d/1jFQbD7Z7vWACuyPVuCjhzhv1HNqyOggG/view?usp=sharing)

## Specifics
The framework of the app was built primarily with [Dash by Plotly](https://dash.plot.ly).

The predictions are generated with ULMFiT models trained on the dataset provided for the
Jigsaw Toxic Comment Classification Kaggle competition.
You can find the dataset [here](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data).

Currently, predictions can be made for 4 types of toxicity:
general toxicity, insults, obscenity, and prejudice/identity hate.

## Usage
Visit the IP address specified above.

If you are trying to run the application locally, use the requirements.txt to build your environment. You also need to provide environment variables that contain credentials for the twitter API  and youtube API. Tweets and youtube comments cannot be collected unless you provide these. Predictions on text entered manually are still possible even without providing the credentials.

These are the necessary environment variables:
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, YOUTUBE_KEY

The first four variables are all for the twitter API. 

You must also download the model and mappings files for each type of toxicity. These files can be downloaded [here](https://1drv.ms/u/s!AuFyq5aZW3rygd5DDrSeTjOea36u9A?e=vaU9Ps). Add them to the "youtoxic/app/models directory".

These files are stored on Onedrive because they are too large for storage on Github and Git LFS has a 1 GB storage limit for free users.

## Documentation
YouToxic uses [Sphinx](http://www.sphinx-doc.org/en/master/) to build the documentation.
To build
```
cd docs
make html
```
