from flask import Blueprint, render_template, redirect, url_for, request

registration = Blueprint("registration", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

usuarios = []
empresas = []

@registration.route("/")
def registration_index():
    return render_template("registration/registration.html")

@registration.route("/add_user", methods=['POST'] )
def registration_register_user():
    global usuarios

    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        email = request.form["email"]
        cpf = request.form["cpf"]
        age = request.form["age"]
        password = request.form["password"]
        confirmPassword = request.form["password2"]

        if password == confirmPassword:
        
            usuarios.append([email,password,username,name,cpf,age,password])

            return redirect(url_for("auth.auth_index"))

@registration.route("/company")
def registration_company():
    return render_template("registration/register_company.html")

@registration.route("/add_company", methods=["POST"])
def registration_add_company():
    global empresas
    if request.method == "POST":
        empresa = request.form["name"]
        if empresa is not None:
            empresas.append(empresa)

            return redirect(url_for("company.company_index"))