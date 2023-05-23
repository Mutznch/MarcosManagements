from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint("auth", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@auth.route("/")
def auth_index():
    return render_template("auth/login.html")

@auth.route("/login", methods=["POST"])
def auth_login():
    return redirect(url_for("company.company_index"))

@auth.route("/signup")
def auth_signup():
    return render_template("auth/signup.html")