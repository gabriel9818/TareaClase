################################################################################################ 
####################################### CLIENTE MQTT ########################################### 
################################################################################################

from paho.mqtt import client as mqtt_client
import random
import json
import time
from geopy.geocoders import Nominatim
import geopy.distance
import geocoder


#Local
#BROKER = 'localhost'
#PORT = 1883
#0TOPIC = "/test"
# generate client ID with pub prefix randomly
#CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
#USERNAME = 'admin'
#PASSWORD = 'public'
#FLAG_CONNECTED = 0

#Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "GRV"
TOPIC_ALERT = "GRV"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0

def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):
    #print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
        ##publish(client,TOPIC_ALERT,"Hola")               

    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    #client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

#Enviar mensajes
def publish(client,TOPIC,msg): 
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)

#Coordenadas en GPS
def obtener_ubicacion_actual():
    ubicacion = geocoder.ip('me')
    return ubicacion.latlng[0], ubicacion.latlng[1]
    
    

#Calcular distancia
LatA,LogA=obtener_ubicacion_actual()
#Simular distancia
LatB=-0.12221231 
LogB=-78.525
#Distancia maxima
DistMax=2
SmSEnviado=False

def obtener_ubicacion_actual():
    ubicacion= geocoder.ip('me')
    return ubicacion.latlng


#client = connect_mqtt()
def run():
    global LatA,LogA, SmSEnviado

    while True:
        client.loop_start()
        time.sleep(1)
        if FLAG_CONNECTED:
            nueva_latitud, nueva_longitud=obtener_ubicacion_actual()
            distance=geopy.distance.distance((LatA,LogA),(LatB,LogB)).meters
            if distance>distance and not SmSEnviado:
                mensaje=("longitud:" , LogA,
                         "latitud:", LatA, 
                         "Distancia:", distance)
                publish(client,TOPIC_ALERT,mensaje)
                SmSEnviado=True
            if distance<distance and not SmSEnviado:
                mensaje=("longitud:" , LogA,
                         "latitud:", LatA, 
                         "Distancia:", distance)
                publish(client,TOPIC_ALERT,mensaje)
                SmSEnviado=True

            lActual=nueva_latitud
            Actual=nueva_longitud

            #print("Wait for message...")

            #print("Wait for message...")
        else:
            client.loop_stop()




if __name__ == '__main__':

    client= connect_mqtt()
    run()