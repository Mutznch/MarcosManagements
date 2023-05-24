from models import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column("id",  db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    cpf = db.Column(db.String(11), min=11, max=11, nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False) 

    roles = db.relationship("Role", back_populates="users", secondary="user_roles")
    reads = db.relationship("Read", backref="users", lazy=True)    
    activations = db.relationship("Activation", backref="users", lazy=True)
    companies = db.relationship("Company", backref="users", lazy=True)
    workers = db.relationship("Worker", backref="users", lazy=True)

    def save_user(username, name, email, cpf, password):

        user = User(username=username, name=name, email=email, cpf=cpf, password=password)

        db.session.add(user)
        db.session.commit()

    def credentials_exists(username, email):
        userEmail = User.query.filter_by(email=email).first()
        userUsername = User.query.filter_by(username=username).first()

        return True if (userEmail or userUsername) else False

    def validate_credentials(login, password):

        user = User.query.filter_by(email=login).first()
        
        if not user:
            user = User.query.filter_by(username=login).first()

        return user if \
            user and \
            check_password_hash(user.password, password) \
            else None

    def get_user_by_id(id):
        user = User.query.filter_by(id=id).first()

        return user

    def get_user_owned_companies(user_id):
        user = User.get_user_by_id(id)
        
        return user.companies