from models import db, Company

class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column("id", db.Integer(), primary_key=True)
    company_id = db.Column(db.Integer(), db.ForeignKey(Company.id))
    name = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(30))
    model = db.Column(db.String(30))
    voltage = db.Column(db.Float(), nullable=False)
    description = db.Column(db.String(512))
    is_active = db.Column(db.Boolean(), nullable=False, default=False)

    sensors = db.relationship("Sensor", backref="devices", lazy=True)
    actuators = db.relationship("Actuator", backref="devices", lazy=True)
    microcontrollers = db.relationship("Microcontroller", backref="devices", lazy=True)