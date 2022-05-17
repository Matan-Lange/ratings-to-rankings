from flask import Blueprint,request
from flask import render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from flask_mail import Message

from app import db, mail
from app.auth.forms import RegisterForm, LoginForm, RecoverPassword
from app.models import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              name=form.name.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              professor_name=form.professor_name.data)

        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Success! you are logged in as :{user_to_create.username}', category='success')

        return redirect(url_for('rating.exp_page'))
    if form.errors != {}:  # if there are no errors from validations
        for err_msg in form.errors.values():
            flash(f'Error found: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! you are logged in as :{attempted_user.username}', category='success')

            return redirect(url_for('rating.exp_page'))
        else:
            flash('User Name and Password are not a match ! try again.', category='danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout_page():
    session.clear()
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for('extra.home_page'))  #


@auth.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    form = RecoverPassword()
    if request.method == 'POST':
        try:
            check_user = db.session.query(User).filter(User.username == form.username.data).all()
            check_email = db.session.query(User).filter(User.email_address == form.email_address.data).all()
            if check_user == check_email:
                msg = Message('Password Recover', recipients=[check_user[0].email_address],
                              body=f'password: {check_user[0].password_hash}')
                mail.send(msg)
                flash('Email sent with password check your inbox', category='success')
                return redirect(url_for('auth.login_page'))
            else:
                flash('Incorrect details', category='danger')
        except:
            flash('System error please try later or contact admin')


    return render_template('recover_password.html', form=form)
