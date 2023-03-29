from flask import Flask, render_template, redirect, url_for, request
from controllers.admin_controller import admin
from controllers.auth_controller import auth
from controllers.company_controller import company
from controllers.registration_controller import registration


app = Flask(__name__, template_folder="./views/", static_folder="./static/")

app.register_blueprint(admin, url_prefix= "/admin")
app.register_blueprint(auth, url_prefix= "/auth")
app.register_blueprint(company, url_prefix= "/company")
app.register_blueprint(registration, url_prefix= "/registration")

@app.route('/')
def index():
    return render_template("home.html")



if __name__ == "__main__":
    app.run(debug=True)