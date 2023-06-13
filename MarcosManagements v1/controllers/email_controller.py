from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers import verifyCompany, verifyOwner

from models import Worker, User, Payment, Company, Email
email = Blueprint("email", __name__, template_folder = './views/', static_folder='./static/', root_path="./")

@email.route("/")
@login_required
def email_index(company_id):
    return render_template("company/email/email_index.html", company_id=company_id, username=current_user.username)

@email.route("/view_emails")
@login_required
def view_emails(company_id):
    emails = Email.get_emails(current_user.id)
    
    return render_template("company/email/view_emails.html", company_id=company_id, emails=emails, username=current_user.username)

@email.route("/view_emails_sent")
@login_required
def view_emails_sent(company_id):
    emails = Email.get_emails_sent(current_user.id)
    
    return render_template("company/email/view_emails.html", company_id=company_id, emails=emails, username=current_user.username)

@email.route("/view_email/<email_id>")
@login_required
def view_email(company_id, email_id):
    email = Email.get_email_by_id(email_id)

    if not email or current_user.id != email.from_id and current_user.id != email.to_id:
        return redirect(url_for("email.email_index", company_id=company_id))

    return render_template("company/email/view_email.html", company_id=company_id, email=email, username=current_user.username)

@email.route("/delete_email/<email_id>")
@login_required
def delete_email(company_id, email_id):
    email = Email.get_email_by_id(email_id)

    if not email or current_user.id != email.from_id and current_user.id != email.to_id:
        return redirect(url_for("email.email_index", company_id=company_id))

    if Email.delete_email(email_id):
        flash("Email Excluído com sucesso!!", "success")
    else:
        flash("Email não pode ser excluído pois está relacionado a leituras salvas no banco!!", "danger")
    return redirect(url_for("email.view_emails", company_id=company_id))

@email.route("/write_email")
@login_required
def write_email(company_id):
    return render_template("company/email/write_email.html", company_id=company_id, username=current_user.username)

@email.route("/save_email", methods = ["POST"])
@login_required
def save_email(company_id):
    to_name = request.form.get("to_name")
    content = request.form.get("content")
    to = User.get_user_by_username(to_name)

    if not to:
        flash("Usuário nao encontrado", "error")
        return redirect(url_for("email.email_index", company_id=company_id))

    Email.save_email(
        from_id=current_user.id, 
        to_id=to.id,
        content=content
    )

    return redirect(url_for("email.view_emails_sent", company_id=company_id))