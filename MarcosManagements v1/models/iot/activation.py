from models import db, User, Actuator

class Activation(db.Model):
    __tablename__ = "activations"
    id = db.Column("activation_id", db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id), primary_key = True)
    actuator_id = db.Column(db.Integer(), db.ForeignKey(Actuator.id), primary_key = True)
    value = db.Column(db.Float())