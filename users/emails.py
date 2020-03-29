from flask_mail import Message
import app
from db import User
from flask import render_template, url_for
from config import INSTANCE_OWNER, MAIL_DEFAULT_SENDER


def send_email_confirm(user: User, token: str):
    confirm_url = url_for("users.verify_token", token=token, _external=True)
    msg = Message(
        "Please confirm your VH7 account",
        recipients=[user.email],
        html=render_template("users/email/confirm.jinja2",
                             confirm_url=confirm_url, user=user),
        sender=(INSTANCE_OWNER, MAIL_DEFAULT_SENDER)
    )
    app.mail.send(msg)
