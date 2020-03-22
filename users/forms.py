"""WTForm form classes for user management."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """WTForm class for logging in a user."""
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")


class RegisterForm(FlaskForm):
    """WTForm class for the creating a new user."""
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=3, max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=40)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6)])
