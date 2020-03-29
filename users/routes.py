"""A file containing the Flask routes for user management."""

from flask import Blueprint, redirect, url_for, request, render_template, abort
from flask import flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import fresh_login_required
from db import db, User
from users.forms import LoginForm, RegisterForm, UpdateAccountForm
from users.forms import DeleteAccountForm
from users.forms import UpdatePasswordForm
from utils.flask_utils import is_safe_url

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Flask route for logging in users."""
    form = LoginForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data.strip()
                                        ).first()
            if user is not None and user.verify_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)

                next = request.args.get("next")
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for("index"))
            else:
                flash("Incorrect username or password!", "error")
    return render_template("users/login.jinja2", form=form)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Flask route for registering new users."""
    form = RegisterForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            user = User(form.username.data.strip(), form.email.data.strip())
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


@user_blueprint.route("/links")
@login_required
def links():
    """Route for viewing the links associated with the current account."""
    short_links = current_user.short_links
    return render_template("users/links.jinja2", links=short_links)


@user_blueprint.route("/account")
@login_required
@fresh_login_required
def account():
    """Flask route for managing the current account."""
    return render_template("users/account.jinja2")


@user_blueprint.route("/account/details", methods=["GET", "POST"])
@login_required
@fresh_login_required
def account_details():
    """Flask route for updating a user's details."""
    form = UpdateAccountForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            if form.username.data.strip() != "":
                current_user.username = form.username.data.strip()

            if form.email.data.strip() != "":
                current_user.email = form.email.data.strip()

            db.session.add(current_user)
            db.session.commit()

            flash("Your account details have been updated successfully",
                  "success")
            return redirect(url_for("users.account"))
    return render_template("users/update_details.jinja2", form=form)


@user_blueprint.route("/account/password", methods=["GET", "POST"])
@login_required
@fresh_login_required
def account_password():
    """Flask route for updating a user's password."""
    form = UpdatePasswordForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            if current_user.verify_password(form.current_password.data):
                current_user.set_password(form.new_password.data)

                db.session.add(current_user)
                db.session.commit()

                flash("Your password has been updated successfully", "success")
                return redirect(url_for("users.account"))
            else:
                flash("Incorrect password!", "error")
    return render_template("users/update_password.jinja2", form=form)


@user_blueprint.route("/account/delete", methods=["GET", "POST"])
@login_required
@fresh_login_required
def account_delete():
    """Flask route for deleting a user."""
    form = DeleteAccountForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            if current_user.username == form.username.data:
                db.session.delete(current_user)
                db.session.commit()

                logout_user()

                flash("Your account has been deleted successfully", "success")
                return redirect(url_for("index"))
            else:
                flash("Incorrect account details!", "error")

    return render_template("users/delete.jinja2", form=form)
