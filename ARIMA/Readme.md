docker build -t arima-forecast .
docker run --name arima -itd  --network ads_network arima-forecast

docker network create ads_network