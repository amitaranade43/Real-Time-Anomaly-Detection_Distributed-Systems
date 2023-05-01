docker build -t outlier-generator .
docker run --name outlier-gen -itd --network ads_network outlier-generator