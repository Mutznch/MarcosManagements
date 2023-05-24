from flask import Blueprint, render_template,redirect,url_for, request, flash
from models import Sensor, Device, Actuator, Microcontroller, db
iot = Blueprint("iot", __name__, template_folder = './views/admin/', static_folder='./static/', root_path="./")

@iot.route("/")
def iot_index():
    return render_template("/iot/iot_index.html")

@iot.route("/register_sensor")
def register_sensor():
    return render_template("/iot/register_sensor.html")

@iot.route("/view_sensors")
def view_sensors(company_id):
    sensors = Sensor.get_company_sensors(company_id)
    return render_template("/iot/view_sensors.html", sensors = sensors)

@iot.route("/save_sensors", methods = ["POST"])
def save_sensors(company_id):
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    description = request.form.get("description")
    measure = request.form.get("measure")
    voltage = request.form.get("voltage")
    is_active = True if request.form.get("is_active") == "on" else False

    Sensor.save_sensor(company_id=company_id, name=name, brand=brand, model=model, description=description ,voltage=voltage, is_active=is_active, measure=measure)

    return redirect(url_for('admin.iot.view_sensors'))

@iot.route("/update_sensor/<id>")
def update_sensor(id):
    sensor = db.session.query(Device, Sensor)\
                        .join(Sensor, Sensor.id == Device.id)\
                        .filter(Sensor.id == int(id)).first()
    
    return render_template("/iot/update_sensor.html", sensor = sensor)

@iot.route("/save_sensor_changes", methods = ["POST"])
def save_sensor_changes():
    data = request.form.copy()
    data["is_active"] = data.get("is_active") == "on"
    Sensor.update_sensor(data)
    return redirect(url_for("admin.iot.view_sensors"))

@iot.route("/delete_sensor/<id>")
def delete_sensor(id):
    if Sensor.delete_sensor(id):
        flash("Dispositivo Sensor Excluído com sucesso!!", "success")
    else:
        flash("Dispositivo Sensor não pode ser excluído pois está relacionado a leituras salvas no banco!!", "danger")
    return redirect(url_for("admin.iot.view_sensors"))


@iot.route("/save_actuator", methods = ["POST"])
def save_actuator(company_id):
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    description = request.form.get("description")
    voltage = request.form.get("voltage")
    is_active = True if request.form.get("is_active") == "on" else False
    actuator_type = request.form.get("actuator_type")
    

    Actuator.save_actuator(company_id=company_id, nmae=name, brand=brand, model=model, description=description , voltage=voltage, is_active=is_active, actuator_type=actuator_type)

    return redirect(url_for('admin.iot.view_actuators'))

@iot.route("/view_actuators")
def view_actuators(company_id):
    actuators = Actuator.get_company_actuators(company_id)
    return render_template("/iot/view_actuators.html", actuators = actuators)

@iot.route("/save_microcontroller", methods = ["POST"])
def save_microcontroller(company_id):
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    description = request.form.get("description")
    voltage = request.form.get("voltage")
    is_active = True if request.form.get("is_active") == "on" else False
    ports = request.form.get("ports")

    Microcontroller.save_microcontroller(company_id=company_id, name=name, brand=brand, model=model, description=description , voltage=voltage, is_active=is_active, ports=ports)

    return redirect(url_for('admin.iot.view_microcontrollers'))

@iot.route("/view_microcontrollers")
def view_microcontrollers(company_id):
    microcontrollers = Microcontroller.get_company_microcontrollers(company_id)
    return render_template("/iot/view_microcontrollers.html", microcontrollers = microcontrollers)

@iot.route("/register_actuator")
def register_actuator():
    return render_template("/iot/register_actuator.html")

@iot.route("/register_microcontroller")
def register_microcontroller():
    return render_template("/iot/register_microcontroller.html")