from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import Length


class EnterTextForm(FlaskForm):
    text = StringField("Enter Text", validators=[Length(min=2)])
    submit = SubmitField("Analyze")
