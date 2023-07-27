import geopy.distance
import geocoder
from paho.mqtt import client as mqtt_client
import random
import time
import json

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "GRV"
TOPIC_ALERT = "GRV"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0

# Coordenadas GPS actuales
def get_current_location():
    # Obtener la ubicación actual basada en las coordenadas GPS
    g = geocoder.ip('me')
    return g.latlng[0], g.latlng[1]

# Obtener la ubicación actual
latitude_a, longitude_a = get_current_location()

# Coordenadas GPS del punto B cercano
latitud_b = -0.229788
longitud_b = -78.525

# Umbrales de distancia
distancia_maxima = 2  # Distancia máxima permitida en metros

# Variable para controlar si se ha enviado el mensaje MQTT
mensaje_enviado = False

# ...

def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc))

def on_message(client, userdata, msg):
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

def publish(client, TOPIC, msg): 
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)

def get_current_location():
    g = geocoder.ip('me')
    return g.latlng

def run():
    global latitude_a, longitude_a, mensaje_enviado

    while True:
        client.loop_start()
        time.sleep(1)

        if FLAG_CONNECTED:
            # Obtener ubicación actual
            nueva_latitud, nueva_longitud = get_current_location()

            # Calcular la distancia entre la ubicación actual y el punto B
            distancia = geopy.distance.distance((latitude_a, longitude_a), (latitud_b, longitud_b)).meters

            # Verificar si la distancia excede el umbral
            if distancia > distancia_maxima and not mensaje_enviado:
                mensaje = ("La trayectoria excede los 2 metros",
                           "longitud: ", longitude_a,
                           "latitud: ",latitude_a,
                           "Distancia: ", distancia)
                publish(client, TOPIC_ALERT, mensaje)
                mensaje_enviado = True
            # else:
            if distancia < distancia_maxima and not mensaje_enviado:
                mensaje = ("longitud: ", longitude_a,
                           "latitud: ",latitude_a,
                           "Distancia: ", distancia)
                publish(client, TOPIC_ALERT, mensaje)
                mensaje_enviado = True
            
            # Actualizar la posición actual
            latitud_actual = nueva_latitud
            longitud_actual = nueva_longitud

        else:
            client.loop_stop()

if __name__ == '__main__':
    # Conectar al MQTT Broker
    client = connect_mqtt()

    # Ejecutar el loop principal
    run()