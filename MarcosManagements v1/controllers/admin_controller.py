from flask import Blueprint, render_template
from controllers.registration_controller import usuarios, empresas
from controllers.company_controller import dispositivos

admin = Blueprint("admin", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@admin.route("/")
def admin_index():
    return render_template("admin/admin.html", users = usuarios, devices = dispositivos, companies = empresas)