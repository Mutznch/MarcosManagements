#https://wokwi.com/projects/367484370141327361

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
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = "aopa"
MQTT_PASSWORD  = "aopa"
MQTT_TOPIC_SEND = "/marcosm/umidade"
MQTT_TOPIC_RECEIVE = "/marcosm/receber"

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)

def callback(topic, msg):
    print("Mensagem recebida: ", msg.decode())
    client.publish(MQTT_TOPIC_RECEIVE) 

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

def moisture():
  sensor.measure()
  moist = ujson.dumps(sensor.humidity())
  return moist
      
def temperature():
  sensor.measure()
  temp = ujson.dumps(sensor.temperature())
  return temp

def light():
  ldrValue = ldr.read()
  return ldrValue

# Pins

sensor = dht.DHT22(Pin(15))
ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)


while True:
  time.sleep(1)
  try:
    mensagem = moisture()
    client.publish(MQTT_TOPIC_SEND, mensagem)
    mensagem = temperature()
    client.publish(MQTT_TOPIC_SEND, mensagem)
    mensagem = str(light())
    client.publish(MQTT_TOPIC_SEND, mensagem)

  except:
    print("Erro")
    pass