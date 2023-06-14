from flask import Blueprint, render_template, request, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Email

auth = Blueprint("auth", __name__, template_folder="./views/", static_folder='./static/', root_path="./")

@auth.route("/")
@login_required
def auth_index():
    return render_template("auth/auth_update.html", user=current_user)

@auth.route("/login")
def auth_login():
    return render_template("auth/login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.auth_login'))

@auth.route("/login_post", methods=["POST"])
def auth_login_post():
    login_info = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.validate_credentials(login=login_info, password=password)

    if not user:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.auth_login'))

    login_user(user, remember=remember)
    
    return redirect(url_for("company.company_index"))

@auth.route("/signup")
def auth_signup():
    return render_template("auth/signup.html")

@auth.route("/signup_post", methods = ["POST"])
def auth_signup_post():
    name = request.form.get("name", None)
    username = request.form.get("username", None)
    email = request.form.get("email", None)
    cpf = request.form.get("cpf", None)
    password = request.form.get("password", None)
    confirm = request.form.get("password2", None)

    

    if len(cpf) != 11:
        flash("CPF inválido", 'error')
        return redirect(url_for('auth.auth_signup'))
    
    try:
        int(cpf)
    except:
        flash("CPF inválido", 'error')
        return redirect(url_for('auth.auth_signup'))

    if User.credentials_exists(username=username, email=email, cpf=cpf):
        flash('Email, Nome de Usuário ou CPF já utilizados', 'error')
        return redirect(url_for('auth.auth_signup'))
    
    if password != confirm:
        flash("Senhas não Batem", 'error')
        return redirect(url_for('auth.auth_signup'))

    User.save_user(name=name, username=username, email=email, cpf=cpf, 
        password=generate_password_hash(password, method='sha256'))

    return redirect(url_for("auth.auth_login"))

@auth.route("/update", methods = ["POST"])
@login_required
def auth_update():
    data = request.form.copy()

    if data['cpf']:
        if len(data['cpf']) != 11:
            flash("CPF inválido", 'error')
            return redirect(url_for('auth.auth_index'))
        
        try:
            int(data['cpf'])
        except:
            flash("CPF inválido", 'error')
            return redirect(url_for('auth.auth_index'))

    if User.credentials_exists(email=data['email'], cpf=data['cpf']):
        flash('Email ou CPF já utilizados', 'error')
        return redirect(url_for('auth.auth_index'))

    if data['password']:
        if data['password'] != data['password2']:
            flash("Senhas não Batem", 'error')
            return redirect(url_for('auth.auth_index'))
        data['password'] = generate_password_hash(data['password'], method='sha256')

    User.update_user(data=data)

    return redirect(url_for("company.company_index"))

@auth.route("/delete")
@login_required
def delete_user():
    if User.delete_user(current_user.id):
        emails = Email.get_emails(current_user.id)
        emails.append(Email.get_emails_sent(current_user.id))
        
        for email in emails:
            Email.delete_email(email.id)

        flash("Usuário Excluído com sucesso!!", "success")
    else:
        flash("Usuário não pode ser excluído pois está relacionado a leituras salvas no banco!!", "danger")
    return redirect(url_for("auth.auth_login"))