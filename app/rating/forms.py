from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField,SelectField , TextAreaField , BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from app.models import User


class RateForm(FlaskForm):
    q1 = TextAreaField(label=':q1', validators=[])

    rate = RadioField('Label',
                    choices=[(1, 'טעון שיפור'), (2, 'סביר'), (3, 'טוב'), (4, 'טוב מאוד'), (5, 'מצוין')],
                    validators=[DataRequired()])

    submit = SubmitField(label='שליחה')


class ChangeText(FlaskForm):
    q1 = TextAreaField(label=':q1', validators=[])

    submit = SubmitField(label='שליחה')


class Compare2(FlaskForm):
    select = RadioField('groupnames',coerce= int,validators=[DataRequired()])
    submit = SubmitField(label='בחירה')