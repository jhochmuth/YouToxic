from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EnterTextForm(FlaskForm):
    text = StringField('Enter Text', validators=[DataRequired()])
    submit = SubmitField("Analyze")
