import paho.mqtt.client as mqtt
import time

# a callback function
def on_message_arima(client, userdata, msg):
    print('Received a new ARIMA data ', msg.payload.decode('utf-8'))


def on_message_bollinger(client, userdata, msg):
    print('Received a new Bollinger data ', str(msg.payload.decode('utf-8')))


def on_message_outlier(client, userdata, msg):
    print('Received a new Outlier data ', str(msg.payload.decode('utf-8')))

def on_message_random(client, userdata, msg):
    print('Received a new Random data ', str(msg.payload.decode('utf-8')))

client = mqtt.Client("greenhouse_server_123")
client.message_callback_add('forecast/arima', on_message_arima)
client.message_callback_add('forecast/bollinger', on_message_bollinger)
client.message_callback_add('forecast/outlier', on_message_outlier)
client.message_callback_add('forecast/random', on_message_random)
# outlier

client.connect('localhost', 1883)
# start a new thread
client.loop_start()
client.subscribe("forecast/#")

while True:
    time.sleep(6)
    # do something you like