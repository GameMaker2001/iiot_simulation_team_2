import paho.mqtt.client as mqtt

import random

import time

 

broker = "localhost"

port = 1883

topic = "sensor/data"

 

def simulate_sensor_data():

    while True:

        temperature = random.uniform(20.0, 25.0)

        humidity = random.uniform(30.0, 50.0)

        payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'

        client.publish(topic, payload)

        time.sleep(1)

 

client = mqtt.Client()

client.connect(broker, port)

simulate_sensor_data()