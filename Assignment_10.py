globals().clear() #clean the environment

from paho.mqtt import client as paho
import paho.mqtt.subscribe as subscribe
import random
import time

broker = 'inet-mqtt-broker.mpi-inf.mpg.de'
port = 1883
client_id = f'irem-gunduz-mqtt-{random.randint(0, 1000)}'
username = 'irgu00001@stud.uni-saarland.de'
password = '7026821'


def connect_broker(client):
  client.username_pw_set(username, password) #set the username and password
  client.connect(broker, port) #connect to the broker using the defined port
  client.loop_start()
  return client

def on_message(client, userdata, msg):  # The callback 
    print("Topic: "+ msg.topic + " Message: " +   str(msg.payload.decode("utf-8")))  # Print a received msg
    client.subscribe(str(msg.payload.decode("utf-8")))
    decoded_payload = str(msg.payload.decode("utf-8"))
    if decoded_payload.startswith("CMD"):
      messg = ""
      if decoded_payload == "CMD1":
        messg = "Apple"
      elif decoded_payload == "CMD2":
        messg = "Cat"
      elif decoded_payload == "CMD3":
        messg = "Dog"
      elif decoded_payload == "CMD4":
        messg = "Rat"
      elif decoded_payload == "CMD5":
        messg = "Boy"
      elif decoded_payload == "CMD6":
        messg = "Girl"
      elif decoded_payload == "CMD7":
        messg = "Toy"
      top = msg.topic + "/" + decoded_payload
      client.subscribe(top)
      client.publish(top,messg)


def run():
    client = paho.Client(client_id) #create new instance
    client.on_message = on_message
    client = connect_broker(client)
    topic = "login"
    msg = "7026821"
    print("Subscribed topic: " + topic)
    client.subscribe("7026821/UUID")
    print("Sent message: " + msg)
    client.publish(topic,msg) #send student id to the topic
    time.sleep(4)
    client.loop_stop()

if __name__ == '__main__':
    run()

            
