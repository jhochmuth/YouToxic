from flask_wtf import FlaskForm

from wtforms import IntegerField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class EnterTextForm(FlaskForm):
    text = StringField('Enter text', validators=[Length(min=2)])
    types = SelectMultipleField('Select classes of toxicity to predict',
                                choices=[('toxic', 'Toxic'), ('identity', 'Identity hate')])
    submit = SubmitField('Calculate predicted toxicity')


class TwitterAccountForm(FlaskForm):
    user = StringField('Enter twitter username', validators=[DataRequired()])
    num_tweets = IntegerField('Enter number of tweets to classify', validators=[NumberRange(min=1, max=3240)])
    types = SelectMultipleField('Select classes of toxicity to predict',
                                choices=[('toxic', 'Toxic'), ('identity', 'Identity hate')])
    submit = SubmitField('Collect tweets')


class ReturnTweetsForm(FlaskForm):
    display = SelectField('Select display mode', choices=[('all', 'All'), ('toxic', 'Toxic only')])
    submit = SubmitField('Confirm')
