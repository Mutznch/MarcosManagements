from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import Sensor, Device, Actuator, Microcontroller, db
from controllers import verifyCompany
from models.iot.mqtt import mqtt_client
iot = Blueprint("iot", __name__, template_folder = './views/', static_folder='./static/', root_path="./")


@iot.route("/")
@login_required
def iot_index(company_id):
    verifyCompany(company_id)
    return render_template("company/iot/iot_index.html", company_id=company_id, username=current_user.username)

@iot.route("/register_sensor")
@login_required
def register_sensor(company_id):
    verifyCompany(company_id)
    return render_template("company/iot/register_sensor.html", username=current_user.username)

@iot.route("/view_sensors")
@login_required
def view_sensors(company_id):
    verifyCompany(company_id)
    sensors = Sensor.get_company_sensors(company_id)
    return render_template("company/iot/view_sensors.html", sensors = sensors, company_id=company_id, username=current_user.username)

@iot.route("/save_sensors", methods = ["POST"])
def save_sensors(company_id):
    verifyCompany(company_id)
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    description = request.form.get("description")
    measure = request.form.get("measure")
    voltage = request.form.get("voltage")
    is_active = True if request.form.get("is_active") == "on" else False

    Sensor.save_sensor(company_id=company_id, name=name, brand=brand, model=model, description=description ,voltage=voltage, is_active=is_active, measure=measure)

    return redirect(url_for('iot.view_sensors', company_id=company_id))

@iot.route("/update_sensor/<id>")
@login_required
def update_sensor(company_id, id):
    verifyCompany(company_id)
    sensor = db.session.query(Device, Sensor)\
                        .join(Sensor, Sensor.id == Device.id)\
                        .filter(Sensor.id == int(id)).first()
    
    return render_template("company/iot/update_sensor.html", sensor = sensor, company_id=company_id, username=current_user.username)

@iot.route("/save_sensor_changes", methods = ["POST"])
def save_sensor_changes(company_id):
    verifyCompany(company_id)
    data = request.form.copy()
    data["is_active"] = data.get("is_active") == "on"
    Sensor.update_sensor(data)
    return redirect(url_for("iot.view_sensors", company_id=company_id))

@iot.route("/delete_sensor/<id>")
def delete_sensor(company_id, id):
    verifyCompany(company_id)
    if Sensor.delete_sensor(id):
        flash("Dispositivo Sensor Excluído com sucesso!!", "success")
    else:
        flash("Dispositivo Sensor não pode ser excluído pois está relacionado a leituras salvas no banco!!", "danger")
    return redirect(url_for("iot.view_sensors", company_id=company_id))

@iot.route("/save_actuator", methods = ["POST"])
def save_actuator(company_id):
    verifyCompany(company_id)
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    description = request.form.get("description")
    voltage = request.form.get("voltage")
    is_active = True if request.form.get("is_active") == "on" else False
    actuator_type = request.form.get("actuator_type")
    

    Actuator.save_actuator(company_id=company_id, nmae=name, brand=brand, model=model, description=description , voltage=voltage, is_active=is_active, actuator_type=actuator_type)

    return redirect(url_for('iot.view_actuators', company_id=company_id))

@iot.route("/view_actuators")
@login_required
def view_actuators(company_id):
    verifyCompany(company_id)
    actuators = Actuator.get_company_actuators(company_id)
    return render_template("company/iot/view_actuators.html", actuators = actuators, company_id=company_id, username=current_user.username)

@iot.route("/save_microcontroller", methods = ["POST"])
def save_microcontroller(company_id):
    verifyCompany(company_id)
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    description = request.form.get("description")
    voltage = request.form.get("voltage")
    is_active = True if request.form.get("is_active") == "on" else False
    ports = request.form.get("ports")

    Microcontroller.save_microcontroller(company_id=company_id, name=name, brand=brand, model=model, description=description , voltage=voltage, is_active=is_active, ports=ports)

    return redirect(url_for('iot.view_microcontrollers', company_id=company_id))

@iot.route("/view_microcontrollers")
@login_required
def view_microcontrollers(company_id):
    verifyCompany(company_id)
    microcontrollers = Microcontroller.get_company_microcontrollers(company_id)
    return render_template("company/iot/view_microcontrollers.html", microcontrollers = microcontrollers, company_id=company_id, username=current_user.username)

@iot.route("/register_actuator")
@login_required
def register_actuator(company_id):
    verifyCompany(company_id)
    return render_template("company/iot/register_actuator.html", company_id=company_id, username=current_user.username)

@iot.route("/register_microcontroller")
@login_required
def register_microcontroller(company_id):
    verifyCompany(company_id)
    return render_template("company/iot/register_microcontroller.html", company_id=company_id, username=current_user.username)

#@iot.route('/messages')
#def check_messages():
#  return render_template("list_reads.html",reads=Read.query.all())

@iot.route('/read_sensor/<sensor_id>')
def publish_message(sensor_id,company_id):

    mqtt_client.publish()

    return redirect(url_for('iot.view_sensors', company_id=company_id))
    #ldr_publish_result = mqtt_client.publish(['/marcosm/luz'], request_data['message'])
    #temp_publish_result = mqtt_client.publish(request_data['/marcosm/temperatura'], request_data['message'])
    
#,ldr_publish_result,temp_publish_result