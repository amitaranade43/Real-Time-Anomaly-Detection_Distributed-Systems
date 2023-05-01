import pandas as pd
import numpy as np
import time
import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid):
    print("Sent EMA Forecasted Data")

mqttClient = mqtt.Client("ema_forecast")
mqttClient.on_publish = on_publish
mqttClient.connect('mosquitto', 1883)
# mosquitto
# start a new thread
mqttClient.loop_start()



df = pd.read_csv("iot_telemetry_data.csv")
df['ts'] = pd.to_datetime(df['ts'], unit='s')
df = df[['ts', 'temp']]

# Simple moving average
sma = df['temp'].rolling(window=20).mean()

# Standard deviation
std = df['temp'].rolling(window=20).std()

upper_bb = sma + 2 * std
lower_bb = sma - 2 * std

df = df.assign(upper_bb=upper_bb, lower_bb=lower_bb)
df.dropna(inplace=True)

while True:
    latest = df.tail(1)
    upper = latest['upper_bb']
    lower = latest['lower_bb']

    rand_num = np.random.uniform(lower, upper)

    # Add uniform noise
    noise_std = 2.0
    noise = np.random.normal(0, noise_std)
    rand_num += noise
    res = float(rand_num)
    
    msg = str(res)
    info = mqttClient.publish(
        topic='forecast/bollinger',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    print(rand_num)

    # Wait for 3 minutes before generating the next number
    time.sleep(60)

