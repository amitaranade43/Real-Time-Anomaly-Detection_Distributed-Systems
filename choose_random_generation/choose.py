import paho.mqtt.client as mqtt
import threading
import numpy as np

# Define the MQTT broker details
broker_address = "mosquitto"
broker_port = 1883

# Define the subscription topics
topic1 = "forecast/arima"
topic2 = "forecast/bollinger"
topic3 = "forecast/outlier"

# Define a dictionary to store the received values
values = {
    topic1: None,
    topic2: None,
    topic3: None
}

# Define a threading.Event object to synchronize the processing
process_event = threading.Event()

# Define the MQTT on_message callback function
def on_message(client, userdata, message):
    global values, process_event
    
    # Store the received value in the values dictionary
    topic = message.topic
    value = message.payload.decode()
    values[topic] = value
    
    # Check if all values have been received
    if None not in values.values():
        # Set the event to signal that processing can proceed
        process_event.set()

# Define the MQTT client
# client = mqtt.Client()
client = mqtt.Client("Choose_Forecast")
# Set the on_message callback function
client.on_message = on_message



# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Subscribe to the topics
client.subscribe(topic1)
client.subscribe(topic2)
client.subscribe(topic3)

# Start the MQTT loop to receive messages
client.loop_start()

# Main loop
while True:
    # Wait for all values to be received
    process_event.wait()

    # Process the received values
    print("Received values:", values)

    # Get the values from the values dictionary
    value1 = values[topic1]
    value2 = values[topic2]
    value3 = values[topic3]

    # Create a list of values
    values_list = [value1, value2, value3]

    # Define the values and their probabilities
    probabilities = [0.45, 0.45, 0.10]

    # Select a random number based on the probabilities
    random_number = np.random.choice(values_list, p=probabilities)

    print("Random number:", random_number)

    def on_publish(client, userdata, mid):
        print("Sent Random Forecasted Data To K-Means")

    mqttClient = mqtt.Client("choose_random_publish_forecast")
    mqttClient.on_publish = on_publish
    mqttClient.connect('mosquitto', 1883)
    mqttClient.loop_start()

    msg = str(random_number)
    info = mqttClient.publish(
        topic='forecast/random',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())

    # Clear the values dictionary
    values = {
        topic1: None,
        topic2: None,
        topic3: None
    }

    # Clear the event to allow for future processing
    process_event.clear()

# Disconnect from the MQTT broker
client.disconnect()

# Stop the MQTT loop
client.loop_stop()
