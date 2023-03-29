from flask import Blueprint, render_template, request, redirect, url_for
from controllers.registration_controller import usuarios

auth = Blueprint("auth", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@auth.route("/")
def auth_index():
    return render_template("auth/login.html")

@auth.route("/login", methods=["POST"])
def auth_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        for u in usuarios:
            if u[0] == email and u[1] == password:
                return redirect("../company")
    return redirect("../auth")