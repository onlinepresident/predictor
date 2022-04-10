from flask_wtf import FlaskForm
from wtforms import (
                     StringField
                    ,PasswordField
                    ,BooleanField
                    ,SubmitField
                    ,TextField
                    ,TextAreaField
                    ,SelectField
                    ,IntegerField
                    ,RadioField
                    ,DecimalField
)
from wtforms.validators import DataRequired,InputRequired,Email
from wtforms.fields.html5 import DateField,EmailField
from datetime import datetime
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Team

class LoginForm(FlaskForm):
    username        = StringField('Username',validators =[DataRequired()])
    password        = PasswordField('Password', validators=[DataRequired()])
    remember_me     = BooleanField('Remember Me')
    submit          = SubmitField('Sign In')

class TeamForm(FlaskForm):
    name = StringField("Team Name", validators=[DataRequired()])
    submit = SubmitField('Add Team')

class PredictionForm(FlaskForm):
    home_team = QuerySelectField(query_factory=lambda: Team.query.all(), allow_blank=True, get_label='name', get_pk = lambda a:a.id, blank_text=u'Select Home Team ...')
    away_team = QuerySelectField(query_factory=lambda: Team.query.all(), allow_blank=True, get_label='name', get_pk = lambda a:a.id, blank_text=u'Select Away Team ...')
    h_odd     = DecimalField("Home Odd")
    d_odd     = DecimalField("Draw Odd")

    submit          = SubmitField('Predict Winner')

class UserForm(FlaskForm):
    username =StringField('Username',validators=[DataRequired()])
    email = EmailField("Email",  validators=[InputRequired("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Add User')
