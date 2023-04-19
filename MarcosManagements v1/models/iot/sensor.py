from models import db, Device

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column('id', db.Integer, db.ForeignKey(Device.id), primary_key=True)
    mesure = db.Column(db.String(20))

    reads = db.relationship("Read", backref="sensors", lazy=True)

    

    def save_sensor(name, brand, model, voltage, description, is_active, measure):
        device = Device(name=name, brand=brand, model = model,
                        voltage = voltage, description = description,
                        is_active = is_active)
        sensor = Sensor(id = device.id, measure = measure)

        device.sensors.append(sensor)

        db.session.add(device)
        db.session.commit()

    def get_sensors():
        sensors = Sensor.query.join(Device, Device.id == Sensor.id)\
                    .add_columns(Sensor.id, Device.name, Device.brand, Device.voltage,
                    Device.model, Sensor.measure).all()
        return sensors
