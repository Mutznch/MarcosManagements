from models import db, Device

class Actuator(db.Model):
    __tablename__ = "actuators"
    id = db.Column("id", db.Integer(), db.ForeignKey(Device.id), primary_key=True)
    actuator_type = db.Column(db.String(30))

    activations = db.relationship("Activation", backref="actuators", lazy=True)

    def get_actuator():
        actuators = Actuator.query\
            .join(Device, Device.id == Actuator.id)\
            .add_columns(
                Actuator.id, 
                Device.name, 
                Device.brand, 
                Device.model, 
                Device.voltage, 
                Device.description,  
                Device.is_active,
                Actuator.actuator_type
        ).all()
        
        return actuators
    
    def save_actuator(company_id, name, brand, model, description, voltage, is_active, actuator_type):
        device = Device(company_id=company_id, name=name, brand=brand, model=model, 
                            description=description, voltage=voltage, is_active=is_active)

        actuator = Actuator(id=device.id, actuator_type=actuator_type)
    
        device.actuators.append(actuator)
        db.session.add(device)
        db.session.commit()