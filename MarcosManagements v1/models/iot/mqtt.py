from flask_mqtt import Mqtt

mqtt_client = Mqtt()
topic_subscribe = ["/marcosm/solo", "/marcosm/luz","/marcosm/temperatura"]