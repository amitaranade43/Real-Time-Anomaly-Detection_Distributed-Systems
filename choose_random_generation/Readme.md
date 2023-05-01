docker build -t choose-random-number .
docker run --name choose-random -itd  --network ads_network choose-random-number
