"""A file containing the Flask routes for user management."""

from flask import Blueprint, redirect, url_for, request, render_template, abort
from flask import flash
from flask_login import login_user, login_required, logout_user, current_user
from db import db, User
from users.forms import LoginForm, RegisterForm
from utils.flask_utils import is_safe_url

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Flask route for logging in users."""
    form = LoginForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)

                next = request.args.get("next")
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for("index"))
            else:
                flash("Incorrect login credentials!", "error")
    return render_template("users/login.jinja2", form=form)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Flask route for registering new users."""
    form = RegisterForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            user = User(form.username.data, form.email.data)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash("Your account has been created, please login.", "info")
            return redirect(url_for("users.login"))
    return render_template("users/register.jinja2", form=form)


@user_blueprint.route("/logout")
@login_required
def logout():
    """Flask route for logging out users."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("index"))
