from flask import Blueprint, render_template, request, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

auth = Blueprint("auth", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@auth.route("/")
def auth_index():
    return render_template("auth/auth_index.html")

@auth.route("/login")
def auth_login():
    return render_template("auth/login.html")

@auth.route("/login_post", methods=["POST"])
def auth_login_post():
    login_info = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.validate_credentials(login=login_info, password=password)

    if not user:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    
    return redirect(url_for("company.company_index"))

@auth.route("/signup")
def auth_signup():
    return render_template("auth/signup.html")

@auth.route("/signup_post", methods = ["POST"])
def auth_signup_post():
    name = request.form.get("name", None)
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    email = request.form.get("email", None)

    if User.credentials_exists(username=username, email=email):
        flash('Email address or username already exists')
        return redirect(url_for('auth.signup'))

    User.save_user(name, username=username, email=email, 
        password=generate_password_hash(password, method='sha256'))

    return redirect(url_for("auth.auth_login"))

# FAZER LOGOUT
# COLOCAR TODAS AS ROTAS LOGIN REQUIRED