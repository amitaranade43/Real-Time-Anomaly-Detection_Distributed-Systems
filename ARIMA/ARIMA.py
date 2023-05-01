from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime
import pandas as pd
import statsmodels.api as sm
import time
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid):
    print("Sent ARIMA Forecasted Data")

mqttClient = mqtt.Client("arima_forecast")
mqttClient.on_publish = on_publish
mqttClient.connect('mosquitto', 1883)
# start a new thread
mqttClient.loop_start()

def arima_analysis(df):
    # Convert UNIX timestamp to datetime format
    df = df.withColumn('ts', from_unixtime('ts'))

    # Keep only 'ts' and 'temp' columns
    df = df.select('ts', 'temp')

    # Convert Spark DataFrame to Pandas DataFrame
    pandas_df = df.toPandas()

    # Perform ARIMA analysis
    model = sm.tsa.ARIMA(pandas_df['temp'], order=(1,0,1)).fit()

    # Forecast the next value
    forecast = model.forecast(steps=1)
    res = forecast.values[0]
    
    msg = str(res)
    info = mqttClient.publish(
        topic='forecast/arima',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())

    # Convert the forecast to a Spark DataFrame and append it to the original dataframe
    schema = StructType([
        StructField('ts', DoubleType(), True),
        StructField('temp', DoubleType(), True)])
    new_row = spark.createDataFrame([(float(time.time()), float(forecast))], schema=schema)
    df = df.union(new_row)

    return df

# Create SparkSession
spark = SparkSession.builder.appName('ARIMA Analysis').getOrCreate()

# Load dataset into a Spark DataFrame
df = spark.read.csv('iot_telemetry_data.csv', header=True, inferSchema=True)

while True:
    # Perform ARIMA analysis and append the forecast to the original dataframe
    df = arima_analysis(df)

    # Print the updated dataframe
    print(df)

    # Wait for 3 minutes before the next iteration
    time.sleep(50)

# Stop SparkSession
spark.stop()
