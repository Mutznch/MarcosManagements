from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers import verifyCompany, verifyOwner

from models import Worker, User, Payment, Company
payment = Blueprint("payment", __name__, template_folder = './views/', static_folder='./static/', root_path="./")

@payment.route("/")
@login_required
def payment_index(company_id):
    verifyCompany(company_id)
    owner = company_id in [str(company.id) for company in User.get_user_owned_companies(current_user.id)]

    return render_template("company/payment/payment_index.html", company_id=company_id, owner=owner, username=current_user.username)

@payment.route("/view_payments")
@login_required
def view_payments(company_id):
    verifyCompany(company_id)
    if company_id in [str(company.id) for company in User.get_user_owned_companies(current_user.id)]:
        payments = Payment.get_company_payments(company_id)
    else: 
        payments = Payment.get_worker_payments(Worker.get_worker_by_user_id(current_user.id, company_id).id)
    
    return render_template("company/payment/view_payments.html", company_id=company_id, payments=payments, username=current_user.username)

@payment.route("/register_payment")
@login_required
def register_payment(company_id):
    verifyOwner(company_id)

    return render_template("company/payment/register_payment.html", company_id=company_id, username=current_user.username)

@payment.route("/confirm_payment", methods = ["POST"])
@login_required
def confirm_payment(company_id):
    verifyOwner(company_id)

    username = request.form.get("username")

    user = User.get_user_by_username(username)
    if not user:
        flash("Nome de usuário em branco", "error")
        return redirect(url_for("payment.register_payment", company_id=company_id))

    worker = Worker.get_worker_by_user_id(user_id=user.id, company_id=company_id)

    if (not worker) or (worker.id not in [worker.id for worker in Company.get_workers(company_id)]):
        flash(f"Usuário {username} não é um funcionário desta empresa", "error")
        return redirect(url_for("payment.register_payment", company_id=company_id))

    return render_template("company/payment/confirm_payment.html", company_id=company_id, name=username, salary=worker.salary, worker_id=worker.id, username=current_user.username)

@payment.route("/save_payment/<worker_id>", methods = ["POST"])
@login_required
def save_payment(company_id, worker_id):
    verifyOwner(company_id)

    Payment.save_payment(worker_id)

    return redirect(url_for("payment.view_payments", company_id=company_id))