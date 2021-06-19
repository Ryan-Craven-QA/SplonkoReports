from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
from app import app


class Api(db.Model):
    # Building API
    apiid = db.Column(db.Integer, primary_key=True)
    apiname = db.Column(db.String(120), index=True, unique=True)         # Stores user inputted Name
    requesttype = db.Column(db.Text, index=True, unique=False)              # Stores request type
    apiurl = db.Column(db.Text, index=True, unique=True)                   # Example:  https://reqres.in/api/users/2
    # apidata = db.Column(db.text, primary_key=True)
    # apijson = db.Column(db.text, primary_key=True)
    # apifiles = db.Column(db.text, primary_key=True)
    # apillowredirects = db.Column(db.Boolean, primary_key=True)
    # apiauth = db.Column(db.text, primary_key=True)
    # apicert = db.Column(db.text, primary_key=True)
    # apicookies = db.Column(db.text, primary_key=True)
    # apiheaders = db.Column(db.text, primary_key=True)
    # apiproxy = db.Column(db.text, primary_key=True)
    #
    # # Storing API Results
    # apirequest = db.Column(db.text, primary_key=True)  #
    # statuscode = db.Column(db.Integer, primary_key=True)  # Status Code: 200, 404
    # apireason = db.Column(db.text, primary_key=True)  # Example would be OK
    # last_run = db.Column(db.DateTime, default=datetime.utcnow)  # Stores date last executed

    # def __repr__(self):
    #     return self.name
    #
    # def set_name(self, name):
    #     return name
    #
    # def set_requesttype(self, requesttype):
    #     return requesttype
    #
    # def set_apiurl(self, apiurl):
    #     return apiurl


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
