"""Forms for flask-feedback."""

from tokenize import String
from wtforms import StringField, PasswordField, SelectField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm
from models import *


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )


class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    

class ReviewForm(FlaskForm):
    """Review for Anime form."""
    
    rating = RadioField("rating", choices=[('1', "★"), ('2', "★"), ('3',"★"), ('4', "★"), ('5', "★")], default = '1'
    )
    comments = StringField("Comments:")


