"""Forms for flask-feedback."""

from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
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
    
    rating = IntegerField(
        "Rating",
        validator={InputRequired(), Length(min=1, max=5)}
    )
    comment = StringField("Comments:")

