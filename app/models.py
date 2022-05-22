from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user

from app import admin
from app import db, login_manger


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# hash algorithem!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=False)
    password_hash = db.Column(db.String(length=60), nullable=False)  # hash algo converts to 60 hash
    professor_name = db.Column(db.String(length=20), nullable=False, unique=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        self.password_hash = plain_text_password

    def check_password_correction(self, attempted_password):
        return self.password_hash == attempted_password


class Group(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.Integer(), nullable=False, unique=True)
    name = db.Column(db.String(length=1024), nullable=False, unique=True)
    professor = db.Column(db.String(length=20), nullable=False, unique=False)


class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.Integer(), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    professor_name = db.Column(db.String(length=20), nullable=False, unique=False)


class Rates(db.Model):
    username = db.Column(db.String(), nullable=False, primary_key=True)
    group = db.Column(db.Integer(), nullable=False, primary_key=True)
    q1 = db.Column(db.String(), nullable=False)
    datetime = db.Column(db.DateTime(), nullable=True)
    rate = db.Column(db.Integer(), nullable=False)


class Rank(db.Model):
    username = db.Column(db.String(), nullable=False, primary_key=True)
    date = db.Column(db.Date(), nullable=False, primary_key=True)
    list_rank = db.Column(db.String(length=1024), nullable=True)
    number_questions = db.Column(db.Integer(), nullable=False, default=0)
    experiment_group = db.Column(db.Integer(), nullable=False, default=1)  # change default to random for review group

class Temp_text(db.Model):
    username = db.Column(db.String(), nullable=False, primary_key=True)
    pickle = db.Column(db.String(), nullable=True)

class MyModelView(ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    # insert admin users!!!!
    def is_accessible(self):
        user = current_user.username
        if user == '313388241' or user == '313354938' or user =='037218898':
            return True
        else:
            return False


admin.add_view(MyModelView(User, db.session,
                           list_columns=['id', 'name', 'username', 'email_address', 'password_hash', 'professor_name'],
                           can_export=True))
admin.add_view(MyModelView(Question, db.session, list_columns=['id', 'number', 'description', 'professor_name']))
admin.add_view(MyModelView(Rates, db.session,
                           list_columns=['username','datetime', 'group', 'q1','rate'], can_export=True))
admin.add_view(MyModelView(Group, db.session, list_columns=['id', 'number', 'name', 'professor']))
admin.add_view(MyModelView(Rank, db.session,
                           list_columns=['username', 'date', 'list_rank', 'number_questions', 'experiment_group'],
                           can_export=True))
admin.add_view(MyModelView(Temp_text, db.session,
                           list_columns=['username', 'pickle'],
                           can_export=True))
