from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EnterTextForm(FlaskForm):
    text = StringField('Enter Text', validators=[Length(min=2)])
    submit = SubmitField('Calculate predicted toxicity')


class TwitterAccountForm(FlaskForm):
    text = StringField('Enter Twitter Username', validators=[DataRequired()])
    submit = SubmitField('Collect tweets')
