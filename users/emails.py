"""Functions for sending emails to users."""
from flask_mail import Message
import app
from db import User
from flask import render_template, url_for
from config import INSTANCE_OWNER, MAIL_DEFAULT_SENDER


def send_email_confirm(user: User, token: str):
    """Send an email asking a user to confirm their email address.

    Args:
        user (User): The user object to send the email to.
        token (str): The email confirmation token.
    """
    confirm_url = url_for("users.verify_token", token=token, _external=True)
    msg = Message(
        "Please confirm your VH7 account",
        recipients=[user.email],
        html=render_template("users/email/confirm.jinja2",
                             confirm_url=confirm_url, user=user),
        sender=(INSTANCE_OWNER, MAIL_DEFAULT_SENDER)
    )
    app.mail.send(msg)


def send_password_reset(user: User, token: str):
    """Send an email asking a user to reset their password.

    Args:
        user (User): The user object to send the email to.
        token (str): The password reset token.
    """
    reset_url = url_for("users.forgot_password_reset", token=token,
                        _external=True)
    msg = Message(
        "Reset your VH7 password",
        recipients=[user.email],
        html=render_template("users/email/forgotten.jinja2",
                             reset_url=reset_url, user=user),
        sender=(INSTANCE_OWNER, MAIL_DEFAULT_SENDER)
    )
    app.mail.send(msg)
