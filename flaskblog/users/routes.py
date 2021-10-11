from flask import Blueprint, render_template, flash, redirect, url_for, request
from flaskblog.users.forms import RegisterationForm, LoginForm, UpdateAccountForm
from flaskblog import bcrypt, db
from flaskblog.models import User
from flaskblog.utils import save_picture
from flask_login import login_user, logout_user, current_user, login_required
users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
            .decode("utf-8")
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your Account has been created", "success")
        return redirect(url_for("users.login"))
        
    return render_template('register.html', form=form, title="register")
        
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You are successfully logged in', 'success')
            return redirect(url_for("main.home"))
        else:
            flash('Either the email donot exist or password is wrong', 'danger')
            return redirect(url_for("users.login"))
    return render_template('login.html', form=form, title="login")

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("users.login"))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.picture.data:
            file_name = save_picture(form.picture.data)
            current_user.image_file = file_name
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for("users.account"))
    return render_template("account.html", form=form, title="Account")
