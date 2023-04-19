from models import db, Device

class Actuator(db.Model):
    __tablename__ = 'actuators'
    id = db.Column('id', db.Integer, db.ForeignKey(Device.id), primary_key=True)
    actuator_type = db.Column(db.String(50))

    activations = db.relationship("Activation", backref="actuators", lazy=True)


    def save_actuator(name, brand, model, voltage, description, is_active, actuator_type):
        device = Device(name=name, brand=brand, model = model,
                        voltage = voltage, description = description,
                        is_active = is_active)
        actuator = Actuator(id = device.id, actuator_type = actuator_type)
        
        device.actuators.append(actuator)

        db.session.add(device)
        db.session.commit()

    def get_actuator():
        actuators = Actuator.query.join(Device, Device.id == Actuator.id)\
                    .add_columns(Actuator.id, Device.name, Device.brand, Device.voltage,
                    Device.model, Actuator.actuator_type).all()
        return actuators