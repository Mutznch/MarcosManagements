from flask import Flask, render_template, redirect, url_for, request
from models.db import db, instance


from controllers.admin_controller import admin
from controllers.auth_controller import auth
from controllers.company_controller import company
from controllers.workers_controller import workers
from controllers.iot_controller import iot

def create_app() -> Flask:
    app = Flask(__name__, 
            template_folder="./views/", 
            static_folder="./static/",
            root_path="./")

    app.config["TESTING"] = False
    app.config["SECRET_KEY"] = "senha ultra secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = instance
    db.init_app(app)

    app.register_blueprint(admin, url_prefix= "/admin")
    app.register_blueprint(auth, url_prefix= "/auth")
    app.register_blueprint(company, url_prefix= "/")
    app.register_blueprint(workers, url_prefix= "/company/<company_id>/workers")
    app.register_blueprint(iot, url_prefix= "/company/<company_id>/iot")

    @app.route('/')
    def index():
        return render_template("home.html")

    return app
