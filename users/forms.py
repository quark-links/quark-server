"""WTForm form classes for user management."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Optional, EqualTo
from users.validators import Unique
from db import User
from wtforms_hcaptcha.fields import HcaptchaField
from config import HCAPTCHA_SITE_KEY, HCAPTCHA_SECRET_KEY


class LoginForm(FlaskForm):
    """WTForm class for logging in a user."""
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    captcha = HcaptchaField(site_key=HCAPTCHA_SITE_KEY,
                            secret_key=HCAPTCHA_SECRET_KEY)


class RegisterForm(FlaskForm):
    """WTForm class for the creating a new user."""
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(min=3, max=50),
                                       Unique(
                                           User,
                                           User.username,
                                           message=("There is already an "
                                                    "account with that "
                                                    "username.")
                                       )])
    email = EmailField("Email",
                       validators=[DataRequired(),
                                   Length(max=100),
                                   Unique(
                                       User,
                                       User.email,
                                       message=("There is already an account "
                                                "with that email.")
                                   )])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(min=6),
                                         EqualTo("password_confirm",
                                                 message="Passwords must match"
                                                 )])
    password_confirm = PasswordField("Repeat Password")
    captcha = HcaptchaField(site_key=HCAPTCHA_SITE_KEY,
                            secret_key=HCAPTCHA_SECRET_KEY)


class UpdateAccountForm(FlaskForm):
    """WTForm class for updating an existing user's details."""
    user_id = None
    username = StringField("Username",
                           validators=[Optional(),
                                       Length(min=3, max=50),
                                       Unique(
                                           User,
                                           User.username,
                                           message=("There is already an "
                                                    "account with that "
                                                    "username.")
                                       )])
    email = EmailField("Email",
                       validators=[Optional(),
                                   Length(max=100),
                                   Unique(
                                       User,
                                       User.email,
                                       message=("There is already an account "
                                                "with that email.")
                                   )])


class UpdatePasswordForm(FlaskForm):
    """WTForm class for updating a user's password."""
    new_password = PasswordField("New Password",
                                 validators=[DataRequired(),
                                             Length(min=6),
                                             EqualTo("password_confirm",
                                                     message=("Passwords must "
                                                              "match"))])
    password_confirm = PasswordField("Repeat New Password")
    current_password = PasswordField("Current Password",
                                     validators=[DataRequired()])


class DeleteAccountForm(FlaskForm):
    """WTForm class for deleting a user."""
    username = StringField("Username", validators=[DataRequired()])


class ForgotPasswordForm(FlaskForm):
    """WTForm class for requesting a password reset email."""
    email = EmailField("Email", validators=[DataRequired(), Length(max=100)])


class ResetPasswordForm(FlaskForm):
    """WTForm class form for resetting a user's password."""
    new_password = PasswordField("New Password",
                                 validators=[DataRequired(),
                                             Length(min=6),
                                             EqualTo("password_confirm",
                                                     message=("Passwords must "
                                                              "match"))])
    password_confirm = PasswordField("Repeat New Password")
