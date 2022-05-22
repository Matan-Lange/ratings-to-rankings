from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField,SelectField , TextAreaField , BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from app.models import User


class RegisterForm(FlaskForm):

    # validate under score will check and do validation - no need to use just need to right correctly

    # def validate_email_address(self, email_address_to_check):
    #     user = User.query.filter_by(email_address=email_address_to_check.data).first()
    #     if user:
    #         raise ValidationError('Email address Exists')

    # def validate_username(self, username_to_check):
    #     user = User.query.filter_by(username=username_to_check.data).first()
    #     if user:
    #         raise ValidationError('Username Exists')

    def validate_password1(self,password1):
        if len(password1.data) < 8:
            raise ValidationError('Password length less then 8 ')

    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Exists')

        if len(username.data) !=9 :
            if len(username.data) !=11 or username.data[0:2] != '99':
                raise ValidationError('User name not valid - use 99  ')







    username = StringField(label=':תעודת זהות', validators=[ DataRequired()])
    name = StringField(label=':שם מלא', validators=[Length(min=0, max=30), DataRequired()])
    email_address = StringField(label=':דואר אלקטורני', validators=[Email(), DataRequired()])
    password1 = PasswordField(label=':סיסמה', validators=[ DataRequired()])
    professor_name = SelectField(':מושב', choices=[('a','24.5 08:00-12:30'),('b','24.5 13:00-16:30'),
                                                      ('c','7.6 09:00-12:30'),('d','7.6 13:00-16:30')])
    approval = BooleanField(label='אישור השתתפות בניסוי', validators=[DataRequired()])
    sumbit = SubmitField(label='הרשמה')


class LoginForm(FlaskForm):
    username = StringField(label=':תעודת זהות', validators=[DataRequired()])
    password = PasswordField(label=':סיסמה', validators=[DataRequired()])
    submit = SubmitField(label='כניסה')


class RecoverPassword(FlaskForm):
    username = StringField(label=':תעודת זהות', validators=[DataRequired()])
    email_address = StringField(label=':דואר אלקטורני', validators=[Email(), DataRequired()])
    submit = SubmitField(label='שליחה')







