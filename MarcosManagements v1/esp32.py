import network
import time
from machine import *
import dht
import ujson
import onewire
import ds18x20
from umqtt.simple import MQTTClient

# MQTT
 

MQTT_CLIENT_ID = "clientId-obEPrlkU74"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = "aopa"
MQTT_PASSWORD  = "aopa"
MQTT_TOPIC_SEND = "/marcosm/solo"
MQTT_TOPIC_RECEIVE = "/marcosm/recieve"

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)

def callback(topic, msg):
    print("Mensagem recebida: ", msg.decode())
    client.publish(MQTT_TOPIC_RECEIVE, "Funcionou!!!!!") 

# Wi-Fi
#WIFI_SSID = ""
#WIFI_PASSWORD = ""

#wifi = network.WLAN(network.STA_IF)
#wifi.active(True)
#wifi.connect(WIFI_SSID, WIFI_PASSWORD)
#while not wifi.isconnected():
#    pass

#print("Conectado à rede Wi-Fi:", WIFI_SSID)
#função com a resposta do topico selecionado


print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)

client.set_callback(callback)

# Tópicos
client.connect()
print("Connected!")
client.subscribe(MQTT_TOPIC_RECEIVE)
client.subscribe(MQTT_TOPIC_SEND)

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
x = 15
y = 14
z = 13

soil = ADC(Pin(x))
ldr = machine.ADC(machine.Pin(y))
temp = ds18x20.DS18X20(onewire.OneWire(machine.Pin(z)))


while True:
  time.sleep(1)
  try:
    #client.check_msg();
    mensagem1 = soilMoisture()
    client.publish(MQTT_TOPIC_SEND, mensagem)
    
    mensagem2 = lightLevel()
    client.publish(MQTT_TOPIC_SEND, mensagem2)

    mensagem3 = temperature()
    client.publish(MQTT_TOPIC_SEND, mensagem3)

  except:
    print("Erro")
    pass