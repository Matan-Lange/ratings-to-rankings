from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, TextAreaField, BooleanField, Field
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask import flash

from app.models import User



class RateForm(FlaskForm):
    q1 = TextAreaField(label=':q1', validators=[])

    rate = RadioField('Label',
                      choices=[(1, 'טעון שיפור'), (2, 'סביר'), (3, 'טוב'), (4, 'טוב מאוד'), (5, 'מצוין')],
                      validators=[DataRequired()])

    range1 = IntegerRangeField(label='range1')
    range2 = IntegerRangeField(label='range2')
    range3 = IntegerRangeField(label='range3')
    range4 = IntegerRangeField(label='range4')
    range5 = IntegerRangeField(label='range5')

    submit = SubmitField(label='שליחה')

    def validate(self):
        sum = self.range1.data + self.range2.data + self.range3.data + self.range4.data + self.range5.data
        if sum == 100:
            return True
        else:
            flash('range should sum up to 100%',category='danger')
            return False



class ChangeText(FlaskForm):
    q1 = TextAreaField(label=':q1', validators=[])

    submit = SubmitField(label='שליחה')


class Compare2(FlaskForm):
    select = RadioField('groupnames', coerce=int, validators=[DataRequired()])
    submit = SubmitField(label='בחירה')
