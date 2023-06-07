from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from controllers import verifyCompany, verifyOwner

from models import Worker, Company, db

workers = Blueprint("workers", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@workers.route("/")
@login_required
def workers_index(company_id):
    verifyCompany(company_id)
    return render_template("company/workers/workers_index.html", company_id=company_id)

@workers.route("/register_worker")
@login_required
def register_workers(company_id):
    verifyCompany(company_id)
    return render_template("company/workers/register_worker.html", company_id=company_id)

@workers.route("/view_workers")
@login_required
def view_workers(company_id):
    verifyCompany(company_id)
    workers = Worker.get_worker_by_company_id(company_id)
    return render_template("company/workers/view_workers.html", workers = workers, company_id=company_id)

@workers.route("/save_worker", methods=["POST"])
def save_worker(company_id):
    verifyCompany(company_id)
    username = request.form.get("username")
    function = request.form.get("function")
    sector = request.form.get("sector")
    working_hours = request.form.get("working_hours")
    salary = request.form.get("salary")

    Worker.save_worker(username=username, company_id=company_id,function=function,sector=sector,working_hours=working_hours,salary=salary)

    return redirect(url_for("workers.view_workers", company_id=company_id))


@workers.route("/update_worker/<worker_id>")
@login_required
def update_worker(worker_id, company_id):
    verifyOwner(company_id)
    worker = Worker.get_worker(worker_id)
    return render_template("company/workers/update_Worker.html", worker=worker, company_id=company_id)

@workers.route("/save_worker_changes", methods = ["POST"])
def save_worker_changes(company_id):
    verifyOwner(company_id)
    data = request.form.copy()
    Worker.save_worker_changes(data)
    return redirect(url_for("workers.view_workers", company_id=company_id))

@workers.route("/delete_worker/<worker_id>")
def delete_worker(company_id, worker_id):
    verifyOwner(company_id)
    if Worker.delete_worker(worker_id):
        flash("Funcionário Excluído com sucesso!!", "success")
    else:
        flash("Funcionário não pode ser excluído pois está relacionado a leituras salvas no banco!!", "danger")
    return redirect(url_for("workers.view_workers", company_id=company_id))
