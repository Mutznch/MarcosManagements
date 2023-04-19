from models import db, Sensor, User
from datetime import datetime

class Read(db.Model):
    __tablename__ = "reads"
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey(User.id), primary_key = True)
    sensor_id = db.Column("sensor_id", db.Integer(), db.ForeignKey(Sensor.id), primary_key = True)
    value = db.Column(db.Float())
    read_datetime = db.Column(db.DateTime(), nullable=False, default=datetime.now())

