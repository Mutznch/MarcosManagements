from flask_login import current_user
from models import Worker, Company
from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash

def verifyCompany(id):
    user_id = current_user.id
    companies = Company.get_my_companies(user_id) + Worker.get_working_companies(user_id)
    companies_id = [str(company.id) for company in companies]
    if id not in companies_id:
        return redirect(url_for('company.company_index'))

def verifyOwner(id):
    user_id = current_user.id
    companies = Company.get_my_companies(user_id)
    companies_id = [str(company.id) for company in companies]
    if id not in companies_id:
        return redirect(url_for('company.company_overview', company_id=id))