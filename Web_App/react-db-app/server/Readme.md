npm start
# or
yarn start


docker build -t ads-server .

docker run --name ads-server -itd -p 4000:4000 --network ads_network ads-server
