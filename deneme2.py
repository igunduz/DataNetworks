globals().clear() #clean the environment

import paho.mqtt.client as mqtt 
import paho.mqtt.subscribe as subscribe
import random
import time

broker = 'inet-mqtt-broker.mpi-inf.mpg.de'
port = 1883
client_id = f'irem-gunduz-mqtt-{random.randint(0, 1000)}'
username = 'irgu00001@stud.uni-saarland.de'
password = '7026821'


def check_con(client, user, flags, rc):
  if rc == 0:
    print("Connected to broker!")
  else:
    print("Connection failed. %d\n", rc)
            
def connect_broker(client_id):
  client = mqtt.Client(client_id) #create new instance
  client.username_pw_set(username, password) #set the username and password
  client.connect(broker, port) #connect to the broker using the defined port
  client.loop_forever()

