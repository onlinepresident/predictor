########### IMPORT SECTION ########################################
from app import db
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
###################################################################

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(128), index=True,unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default = False)

    predictions = db.relationship('Prediction',  backref='predictor', lazy='dynamic')

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(200))

    def __repr__(self):
        return '<Team: {}>'.format(self.name)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(32), unique=True)
    home_team       = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team       = db.Column(db.Integer, db.ForeignKey('team.id'))
    winner = db.Column(db.String(32))
    insert_date = db.Column(db.DateTime,index=True, default = datetime.utcnow)

    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Prediction: {}>'.format(self.winner)


class PredictionView(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    home_team = db.Column(db.String(200))
    away_team=db.Column(db.String(200))
    winner = db.Column(db.String(200))
    prediction_date = db.Column(db.DateTime, index=True,default = datetime.utcnow)
    username = db.Column(db.String(200))
    user_id = db.Column(db.Integer)
    # # id, home_team, away_team, winner, prediction_date, username, user_id
