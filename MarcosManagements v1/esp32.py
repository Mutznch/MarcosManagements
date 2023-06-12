import network
import time
from machine import *
import dht
import onewire
import ds18x20
from umqtt.simple import MQTTClient

# Wi-Fi
WIFI_SSID = ""
WIFI_PASSWORD = ""

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    pass

print("Conectado à rede Wi-Fi:", WIFI_SSID)

# MQTT
#def callback(topic, msg):
#    print("Mensagem recebida: ", msg.decode())
#    client.publish(MQTT_TOPIC_RECEIVE, "ok")  # Envia "ok" como resposta

MQTT_CLIENT_ID = ""
MQTT_BROKER    = ""
MQTT_USER      = ""
MQTT_PASSWORD  = ""
#MQTT_TOPIC_SEND = ""
MQTT_TOPIC_RECEIVE = ""

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
#client.set_callback(callback)

# Tópicos
  client.connect()
  client.subscribe(MQTT_TOPIC_RECEIVE)

# Mensagem
def mensagem(MQTT_TOPIC_SEND,arg):
  client.publish(MQTT_TOPIC_SEND, arg)

# Funções
def soilMoisture():
  soilValue = soil.read()
  return soilValue
      
def lightLevel():
  ldrValue = ldr.read()
  return ldrValue

def temperature():
  tempValue = temp.convert_temp()
  time.sleep(2)
  return temp.read_temp(tempValue)

# Pins
x = 13
y = 14
z = 15
soil = machine.ADC(machine.Pin(x))
ldr = machine.ADC(machine.Pin(y))
temp = ds18x20.DS18X20(onewire.OneWire(machine.Pin(z)))


while True:
  try:
      mensagem("/marcosm/solo",soilMoisture)
      mensagem("/marcosm/luz",lightLevel)
      mensagem("/marcosm/temperatura",temperature)
  except:
    print("Erro")
    pass