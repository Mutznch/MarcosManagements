from flask import Flask, render_template, redirect, url_for, request
from models.db import db, instance
from flask_login import LoginManager, current_user 
from models import Read 
from datetime import datetime

from controllers.admin_controller import admin
from controllers.auth_controller import auth
from controllers.company_controller import company
from controllers.workers_controller import workers
from controllers.iot_controller import iot
from controllers.payment_controller import payment
from controllers.email_controller import email
from models.iot.mqtt import mqtt_client, topic_subscribe


def create_app() -> Flask:
    app = Flask(__name__, 
            template_folder="./views/", 
            static_folder="./static/",
            root_path="./")

    app.config["TESTING"] = False
    app.config["SECRET_KEY"] = "senha ultra secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = instance
    app.config['MQTT_BROKER_URL'] = "broker.hivemq.com"
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ""  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ""  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True


    mqtt_client.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.auth_login"
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.register_blueprint(admin, url_prefix= "/admin")
    app.register_blueprint(auth, url_prefix= "/auth")
    app.register_blueprint(company, url_prefix= "/")
    app.register_blueprint(workers, url_prefix= "/company/<company_id>/workers")
    app.register_blueprint(iot, url_prefix= "/company/<company_id>/iot")
    app.register_blueprint(payment, url_prefix= "/company/<company_id>/payment")
    app.register_blueprint(email, url_prefix= "/company/<company_id>/email")

    @app.route('/')
    def index():
        return render_template("/home.html", auth = current_user.username if current_user.is_authenticated else False)
    
    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected successfully')
            for topic in topic_subscribe:   
                mqtt_client.subscribe(topic) # subscribe topic
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        print("bolas")
        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        if(message.topic in ["/marcosm/umidade"]):
            with app.app_context():

                print("deu certo")
                reads = Read(user_id=1,sensor_id=1,value=message.payload.decode())
                db.session.add(reads)
                db.session.commit()

    return app
