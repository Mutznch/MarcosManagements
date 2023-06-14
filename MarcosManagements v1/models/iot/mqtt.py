from flask_mqtt import Mqtt

mqtt_client = Mqtt()
topic_subscribe = ["/marcosm/umidade","/marcosm/receber"]