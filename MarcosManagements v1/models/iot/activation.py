from models import db, User, Actuator
from datetime import datetime

class Activation(db.Model):
    __tablename__ = "activations"
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey(User.id), primary_key = True)
    actuator_id = db.Column("actuator_id", db.Integer(), db.ForeignKey(Actuator.id), primary_key = True)
    activation_datetime = db.Column(db.DateTime(), nullable=False, default=datetime.now())