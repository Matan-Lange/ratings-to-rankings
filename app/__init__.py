from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView
import os



app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI') # cloud
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.secret_key = b'################'


app.config['DEBUG'] = True
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True #securty
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] =os.environ.get('MAIL_USERNAME')
app.config['MAIL_MAX_EMAILS'] = 5 # max_mails
app.config['MAIL_SUPPRESS_SEND'] = False  #stop sending when testing
app.config['MAIL_ASCI_ATTACHMENTS'] = False #CONVERTS FILE NAME TO ASSCI

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #hash passwords
login_manger = LoginManager(app)
login_manger.login_view = 'auth.login_page'
login_manger.login_message_category = "info"

admin = Admin(app)
mail = Mail(app)


from app.auth.routes import auth
from app.rating.routes import rating
from app.extra.routes import extra

app.register_blueprint(auth)
app.register_blueprint(rating)
app.register_blueprint(extra)