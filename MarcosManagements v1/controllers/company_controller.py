from flask import Blueprint, render_template, request, redirect, url_for

company = Blueprint("company", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@company.route("/")
def company_index():
    return render_template("company/company_index.html")

#não existe, mas deve estar no workers
'''@company.route("/manage_workers")
def company_manage_workers():
    return render_template("company/manage_workers.html", workers = funcionarios)'''
#outdated, criar iot controller?
#não tem register device e sim varias paginas pra cada um
'''
@company.route("/register_device")
def company_register_device():
    return render_template("company/register_device.html")

@company.route("/add_device",  methods=['POST'])
def company_add_device():
    if request.method == "POST":
        device = request.form["name"]
        if device is not None:
            dispositivos.append(device)

            return redirect("manage_devices")

@company.route("/manage_devices")
def company_manage_devices():
    return render_template("company/manage_devices.html", devices = dispositivos)'''