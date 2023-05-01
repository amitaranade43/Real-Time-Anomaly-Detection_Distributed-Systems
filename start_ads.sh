#!/bin/bash
docker run --name db-postgres -e POSTGRES_PASSWORD=root -p 5433:5432 -v /Users/stevemendis/Desktop/ADS_Final/db/abnormal.sql:/docker-entrypoint-initdb.d/abnormal.sql -d --network ads_network postgres:latest
docker run -itd --name mosquitto -p 1883:1883 --network ads_network -v /Users/stevemendis/Desktop/ADS_Final/mqtt/docker-mosquitto/mosquitto:/mosquitto/ eclipse-mosquitto
docker run --name arima -itd  --network ads_network arima-forecast
docker run --name ema -itd  --network ads_network bollinger-forecast
docker run --name outlier-gen -itd --network ads_network outlier-generator
docker run --name choose-random -itd  --network ads_network choose-random-number
docker run --name ads-server -itd -p 4000:4000 --network ads_network ads-server
docker run --name ads-client -itd -p 3000:3000 --network ads_network ads-client
docker run --name k-means -itd  --network ads_network k-means