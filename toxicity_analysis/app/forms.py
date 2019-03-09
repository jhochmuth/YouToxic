from flask_wtf import FlaskForm

from wtforms import IntegerField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class EnterTextForm(FlaskForm):
    """Defines form that requests text for basic predictions."""
    text = StringField('Enter text', validators=[Length(min=2)])
    types = SelectMultipleField('Select classes of toxicity to predict',
                                choices=[('toxic', 'Toxic'), ('identity', 'Identity hate')])
    submit = SubmitField('Calculate predicted toxicity')


class TwitterAccountForm(FlaskForm):
    """Defines form that requests information for tweet analysis."""
    user = StringField('Enter twitter username', validators=[DataRequired()])
    num_tweets = IntegerField('Enter number of tweets to classify', validators=[NumberRange(min=1, max=3240)])
    types = SelectMultipleField('Select classes of toxicity to predict',
                                choices=[('toxic', 'Toxic'), ('identity', 'Identity hate')])
    submit = SubmitField('Collect tweets')


class ReturnTweetsForm(FlaskForm):
    """Defines form that requests display mode for tweet analysis (all or only toxic)."""
    display = SelectField('Select display mode', choices=[('all', 'All'), ('toxic', 'Toxic only')])
    submit = SubmitField('Confirm')
