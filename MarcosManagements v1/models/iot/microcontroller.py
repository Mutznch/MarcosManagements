from models import db, Device

class Microcontroller(db.Model):
    __tablename__ = "microcontrollers"
    id = db.Column("id", db.Integer(), db.ForeignKey(Device.id), primary_key=True)
    ports = db.Column(db.Integer())

    alerts = db.relationship("Alert", backref="microcontrollers", lazy=True)

    def get_microcontroller():
        microcontrollers = Microcontroller.query\
            .join(Device, Device.id == Microcontroller.id)\
            .add_columns(
                Microcontroller.id,
                Device.name, 
                Device.brand, 
                Device.model, 
                Device.voltage, 
                Device.description,  
                Device.is_active,
                Microcontroller.ports
        ).all()
        
        return microcontrollers
    
    def save_microcontroller(company_id, name, brand, model, description, voltage, is_active, ports):
        device = Device(company_id=company_id, name=name, brand=brand, model=model, 
                            description=description, voltage=voltage, is_active=is_active)
    
        microcontroller = Microcontroller(id=device.id, ports=ports)
        
        device.microcontrollers.append(microcontroller)
        db.session.add(device)
        db.session.commit()