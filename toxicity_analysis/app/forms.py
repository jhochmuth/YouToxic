from flask_wtf import FlaskForm

from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class EnterTextForm(FlaskForm):
    text = StringField('Enter Text', validators=[Length(min=2)])
    submit = SubmitField('Calculate predicted toxicity')


class TwitterAccountForm(FlaskForm):
    user = StringField('Enter Twitter Username', validators=[DataRequired()])
    num_tweets = IntegerField('Enter Number of Tweets to Classify', validators=[NumberRange(min=1, max=3240)])
    submit = SubmitField('Collect tweets')
