from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Worker, Company, db

workers = Blueprint("workers", __name__, template_folder="./views/", static_folder='./static/', root_path="./company/")

@workers.route("register_worker")
def register_workers():
    return render_template("company/workers/register_worker.html")

@workers.route("save_worker", method=["POST"])
def save_worker():
    username = request.form.get("username")
    function = request.form.get("function")
    sector = request.form.get("sector")
    working_hours = request.form.get("working_hours")
    salary = request.form.get("salary")

    Worker.save_worker(username,function,sector,working_hours,salary)

    return redirect(url_for("company.company_index"))



@workers.route("update_worker/{{ worker.id }}")
def update_worker(id):
    worker = db.session.query(Worker, Company)\
                        .join(Company, Company.id == Worker.id)\
                        .filter(Company.id == int(id)).first()
    
    return render_template("company/workers/update_Worker.html", workers = worker)

@workers.route("save_worker_changes", methods = ["POST"])
def save_worker_changes():
    data = request.form.copy()
    Worker.save_worker_changes(data)
    return redirect(url_for("company.company_index"))

@workers.route("delete_worker/{{ worker.id }}")
def delete_worker(id):
    if Worker.delete_worker(id):
        flash("Funcionário Excluído com sucesso!!", "success")
    else:
        flash("Funcionário não pode ser excluído pois está relacionado a leituras salvas no banco!!", "danger")
    return redirect(url_for("company.company_index"))
