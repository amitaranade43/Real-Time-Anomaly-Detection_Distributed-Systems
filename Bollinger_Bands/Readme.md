docker build -t bollinger-forecast .
docker run --name ema -itd  --network ads_network bollinger-forecast