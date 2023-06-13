from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Company, Worker
from controllers import verifyCompany, verifyOwner

company = Blueprint("company", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@company.route("/company")
@login_required
def company_index():
    user_id = current_user.id

    owned_companies = Company.get_my_companies(user_id)
    employed_companies = Worker.get_working_companies(user_id)
    
    return render_template("company/companies.html", owned_companies=owned_companies, employed_companies=employed_companies, user_id = current_user.id, auth = current_user.username if current_user.is_authenticated else False)

@company.route("/company/<id>")
@login_required
def company_overview(id):
    verifyCompany(id)
    return render_template("company/company_index.html", company_id=id, username=current_user.username)

@company.route("/register")
@login_required
def company_register_company():
    return render_template("company/register_company.html", user_id = current_user.id)

@company.route("/save_company", methods=["POST"])
@login_required
def company_save_company():

    name = request.form.get("name")

    Company.save_company(owner_id=current_user.id,name=name)

    return redirect(url_for("company.company_index"))

@company.route("/company/save_company_changes/<company_id>", methods=["POST"])
@login_required
def company_save_company_changes(company_id):
    verifyOwner(company_id)

    name = request.form.get("name")

    Company.update_company(id=company_id, name=name)

    return redirect(url_for("company.company_index"))

@company.route("/company/delete/<company_id>", methods=["POST"])
@login_required
def delete_company(company_id):
    verifyOwner(company_id)

    if Company.delete_company(company_id):
        flash("Empresa Excluída com sucesso!!", "success")
    else:
        flash("Empresa não pode ser excluída pois está relacionado a leituras salvas no banco!!", "danger")
    return redirect(url_for("company.company_index"))

@company.route("/company/update/<company_id>")
@login_required
def company_update_company(company_id):
    verifyOwner(company_id)

    return render_template("company/company_update.html", user_id = current_user.id, company=Company.get_company_by_id(company_id), company_id=company_id)