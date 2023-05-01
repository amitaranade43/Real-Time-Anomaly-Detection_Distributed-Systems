docker build -t k-means .

docker run --name k-means -itd  --network ads_network k-means