from flask import Blueprint, render_template, request, redirect, url_for

company = Blueprint("company", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@company.route("/company")
def company_index():
    # Metodos pegar Companies que o usuario trabalha
    # Passar owned companies e employed companies no render template
    return render_template("company/companies.html")

@company.route("/company/<id>")
def company_overview():
    return render_template("company/company_index.html")

@company.route("/register")
def company_register_company():
    return render_template("company/register_company.html")

@company.route("/save_company")
def company_save_company():
    # Metodo para salvar Company
    return redirect(url_for("company.company_index"))