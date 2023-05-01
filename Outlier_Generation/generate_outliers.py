import pandas as pd
import numpy as np
from scipy.stats import norm
import time
import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid):
    print("Sent Oultier Forecasted Data")

mqttClient = mqtt.Client("outlier_forecast")
mqttClient.on_publish = on_publish
mqttClient.connect('mosquitto', 1883)
# mosquitto
# start a new thread
mqttClient.loop_start()

while True:
    # Load the data from the CSV file
    data = pd.read_csv("iot_telemetry_data.csv")
    temperature_data = data["temp"]

    # Calculate the mean and standard deviation of the temperature data
    mu, std = norm.fit(temperature_data)

    # Generate a lower outlier
    lower_outlier = np.random.normal(mu - 6 * std, std)
    print("Lower outlier:", lower_outlier)

    # Generate a higher outlier
    higher_outlier = np.random.normal(mu + 20 * std, std)
    print("Higher outlier:", higher_outlier)
    l = [lower_outlier, higher_outlier]
    random_number = float(np.random.choice(l))

    msg = str(random_number)
    info = mqttClient.publish(
        topic='forecast/outlier',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())

    # Wait for 3 minutes before generating the next random number
    time.sleep(60)
