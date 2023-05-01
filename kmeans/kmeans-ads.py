import pyspark
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import when
from pyspark.sql.functions import udf, lit
from pyspark.sql.types import StringType
import pickle
import pandas as pd
from pyspark.ml.clustering import KMeansModel
import paho.mqtt.client as mqtt
import queue
import psycopg2
import random

# Create a UDF that takes a column and returns a string value
def check_category(column, min_temp, second_max_temp):
    if column < min_temp or column > second_max_temp:
        return "Abnormal"
    else:
        return "Normal"


def kmeans_train(df1):
    df = df1.select("Temperature")

    assemble = VectorAssembler(inputCols=['Temperature'], outputCol='features')
    assembled_data = assemble.transform(df)
    # assembled_data.show(2)

    silhouette_score = []
    evaluator = ClusteringEvaluator(predictionCol='prediction', featuresCol='features',
                                    metricName='silhouette', distanceMeasure='squaredEuclidean')

    for i in range(4, 10):
        KMeans_algo = KMeans(k=i)
        KMeans_fit = KMeans_algo.fit(assembled_data)
        output = KMeans_fit.transform(assembled_data)

        score = evaluator.evaluate(output)
        silhouette_score.append(float(score))
        # print("Silhouette Score:",score)

    max_score = max(silhouette_score)
    ideal_k = silhouette_score.index(max_score)+4
    # print(ideal_k)

    # Visualizing the silhouette scores in a plot
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.plot(range(4, 10), silhouette_score)
    ax.set_xlabel('k')
    ax.set_ylabel('cost')

    kmeans = KMeans(k=ideal_k, seed=1)
    model = kmeans.fit(assembled_data)

    output = model.transform(assembled_data)

    max_temperature = output.groupBy("prediction").agg(
        pyspark.sql.functions.max("Temperature"))
    max_temperature.show()

    # max_temperature.select("Temperature").tolist()
    max_list = max_temperature.toPandas()["max(Temperature)"].tolist()

    sorted_temp_list = sorted(max_list)
    min_temp = sorted_temp_list[0]
    second_max_temp = sorted_temp_list[-2]

    # Create a column called "Category" that is the result of calling the UDF on the "prediction" column
    output = output.withColumn("Category", udf(check_category, StringType())(
        output.Temperature, lit(min_temp), lit(second_max_temp)))

    model.save("kmeans_model")

    newFile = output.select("Temperature", "prediction", "Category")
    finalFile = newFile.repartition(1)
    finalFile.write.csv("labeledData.csv", header=True)

    with open("model.pkl", "wb") as f:
        pickle.dump(max_list, f)

    centers = model.clusterCenters()
    labels = model.transform(assembled_data).select("prediction").toPandas()

    # Create a Pandas DataFrame that contains the original data and its assigned cluster label
    df = pd.DataFrame(assembled_data.toPandas())
    df["label"] = labels["prediction"]

    # Plot the data points and color them based on their assigned cluster label
    # plt.scatter(df["Temperature"], [0] * len(df), c=df["label"])
    # plt.scatter(centers, [0] * len(centers), marker="x",
    #             s=200, linewidths=3, color="r")
    # plt.xlabel('Temperature in Celcius')
    # plt.ylabel(" ")
    # plt.show()
    # labels = [int(row.prediction)
    #           for row in output.select("prediction").collect()]


def kmeans_predict(temperature, spark):
    kmeans_model = KMeansModel.load("kmeans_model")
    df1 = spark.createDataFrame([[temperature]],
                                ["Temperature"])
    vecAssembler = VectorAssembler(
        inputCols=["Temperature"], outputCol="features")
    new_df1 = vecAssembler.transform(df1)
    final_result = kmeans_model.transform(new_df1)

    # Load the pickle file to get max temp value of each cluster
    with open("model.pkl", "rb") as f:
        max_temp_list = pickle.load(f)
        # print(max_temp_list)

    sorted_temp_list = sorted(max_temp_list)
    min_temp = sorted_temp_list[0]
    second_max_temp = sorted_temp_list[-2]
    # print(max_temp_val)

    # Create a column called "Category" that is the result of calling the UDF on the "prediction" column
    final_result = final_result.withColumn("Category", udf(check_category, StringType())(
        final_result.Temperature, lit(min_temp), lit(second_max_temp)))

    return final_result.collect()[0][3]

def on_message_random(client, userdata, msg):
    print('Received a new Random data ', str(msg.payload.decode('utf-8')))
    msg_queue.put(float(msg.payload.decode('utf-8')))
    # print(result)

def main():
    spark = SparkSession.builder.appName(
        'Clustering using K-Means').getOrCreate()
    df1 = spark.read.csv('iot_telemetry_data.csv',
                         header=True, inferSchema=True)
    # kmeans_train(df1)
    while True:
        
        temp_mqtt = client.message_callback_add('forecast/random', on_message_random)
        # outlier
        print(type(temp_mqtt))
        try:
            temperature = msg_queue.get(timeout=20.0)
            result = kmeans_predict(temperature, spark)
            if result == "Normal":
                pass
            else:
                random_number = random.randint(1, 50)
                
                # create a cursor object to execute PostgreSQL commands
                cur = conn.cursor()
                
                # execute the INSERT command
                cur.execute("INSERT INTO abnormal_table (temp, server_id, status) VALUES (%s, %s, %s)", (temperature, random_number , True))

                # commit the changes to the database
                conn.commit()

                # close the cursor and connection
                
        except queue.Empty:
            pass
        
    spark.stop()
    cur.close()
    conn.close()

if __name__ == "__main__":
    conn = psycopg2.connect(
            database="postgres", 
            user="postgres", 
            password="root", 
            host="db-postgres", 
            port="5432")
    msg_queue = queue.Queue()
    client = mqtt.Client("kmeans-subscribe")
    client.connect('mosquitto', 1883)
    # start a new thread
    client.loop_start()
    client.subscribe("forecast/#")
    main()
