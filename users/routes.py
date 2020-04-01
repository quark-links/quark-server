"""A file containing the Flask routes for user management."""

from flask import Blueprint, redirect, url_for, request, render_template, abort
from flask import flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import fresh_login_required
from db import db, User
from users.forms import LoginForm, RegisterForm, UpdateAccountForm
from users.forms import DeleteAccountForm, UpdatePasswordForm
from users.forms import ForgotPasswordForm, ResetPasswordForm
from utils.flask_utils import is_safe_url
import utils.email_token as email_token
import datetime
import users.emails as email

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Flask route for logging in users."""
    form = LoginForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data.strip()
                                        ).first()
            if user is None or not user.verify_password(form.password.data):
                flash("Incorrect username or password!", "error")
            elif not user.active:
                flash("Sorry, your account is currently disabled.", "error")
            elif not user.confirmed:
                flash(("Sorry, your account does not have a confirmed email "
                       "yet. Please check your emails to confirm."), "warning")

                token = email_token.generate_confirmation_token(user)
                email.send_email_confirm(user, token)
            else:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)

                next = request.args.get("next")
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for("index"))

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

            token = email_token.generate_confirmation_token(user)
            email.send_email_confirm(user, token)

            flash(("Your account has been created. You must verify your email "
                   "address before you can login."), "info")
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
                current_user.confirmed = False
                current_user.confirmed_on = None
                current_user.email = form.email.data.strip()

                token = email_token.generate_confirmation_token(current_user)
                email.send_email_confirm(current_user, token)

                flash("Your email address has been updated. Please check your "
                      "emails to confirm your new email address.", "info")

            db.session.add(current_user)
            db.session.commit()

            flash("Your account details have been updated successfully.",
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


@user_blueprint.route("/verify/<token>")
def verify_token(token):
    """Flask route for verifying a user's email."""
    user = email_token.verify_confirmation_token(token)
    if not user:
        flash(("The confirmation link is invalid, has expired or has already "
               "been used."), "danger")
        return redirect(url_for("users.login"))

    user.clear_tokens()

    if user.confirmed:
        flash("Your account has already been confirmed.",
              "success")
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        flash("Thanks! Your account's email address has been confirmed." +
              (" You may now login." if current_user.is_authenticated else ""),
              "success")

    db.session.add(user)
    db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for("users.account"))
    else:
        return redirect(url_for("users.login"))


@user_blueprint.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    """Flask route for requesting a password reset email."""
    form = ForgotPasswordForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user is not None:
                token = email_token.generate_password_reset_token(user)
                email.send_password_reset(user, token)
                flash(("A password reset email has been sent. Please check "
                       "your inbox"), "success")
            else:
                flash("Sorry, there are no users with that email address.",
                      "warning")

    return render_template("users/request_password_reset.jinja2", form=form)


@user_blueprint.route("/forgot/<token>", methods=["GET", "POST"])
def forgot_password_reset(token):
    """Flask route for resetting a users password with a token."""
    form = ResetPasswordForm(request.form)
    user = email_token.verify_password_reset_token(token)

    if not user:
        flash(("The password reset link is invalid, has expired or has already"
               " been used."), "error")
        return redirect(url_for("users.login"))

    if request.method == "POST":
        if form.validate_on_submit():
            user.set_password(form.new_password.data)
            user.clear_tokens()
            db.session.add(user)
            db.session.commit()

            flash(("Your password has been successfully updated. You may now "
                   "login."), "success")
            return redirect(url_for("users.login"))

    return render_template("users/password_reset.jinja2", form=form,
                           token=token)
