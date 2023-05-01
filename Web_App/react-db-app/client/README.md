npm start

docker build -t ads-client .

docker run --name ads-client -itd -p 3000:3000 --network ads_network ads-client
