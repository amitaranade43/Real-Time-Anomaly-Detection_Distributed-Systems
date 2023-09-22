# Applied-distributed-systems-project
In this project, we have implemented a comprehensive data analysis system that generates random numbers using statistical models such as EMA-bollinger bands, ARIMA, and outlier detection. The generated data is then put into a MQTT queue and collected for analysis. K-means clustering is performed on the data, and the output generated is stored in a database. Finally, the results are displayed on a user interface, which shows the abnormal/normal status of the data using ReactJS.

We have explored three different messaging protocols: MQTT, Kafka, and CoAP. Overall, MQTT is suitable for small-scale IoT deployments, Kafka is suitable for big data applications, and CoAP is suitable for resource-constrained IoT devices. We have chosen MQTT for our project since we have chosen small dataset of a telemetry company.

### Technical Flow-

EMA-bollinger bands, ARIMA, and outlier detection for generating random numbers

MQTT queue for collecting the generated data

K-means clustering for analyzing the data

Database for storing the output of the analysis

ReactJS for displaying the abnormal/normal status of the data on a user interface

Docker for containerizing the entire system


### Dataflow Diagram-

![image](https://github.com/amitaranade43/Real-Time-Anomaly-Detection_Distributed-Systems/assets/34507621/c649f676-f031-4916-9c47-7b5613a658fc)


#### To run individual containers use this command  ./start_ads.sh 

#### To run using the docker-compose use the following command docker-compose up
