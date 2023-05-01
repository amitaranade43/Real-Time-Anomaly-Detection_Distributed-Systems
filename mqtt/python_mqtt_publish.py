import time
import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid):
    print("sent a message")


mqttClient = mqtt.Client("greenhouse_alarm")
mqttClient.on_publish = on_publish
mqttClient.connect('localhost', 1883)
# start a new thread
mqttClient.loop_start()

# Why use msg.encode('utf-8') here
# MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
# Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
while True:
    msg = "29"
    info = mqttClient.publish(
        topic='forecast/random',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(30)