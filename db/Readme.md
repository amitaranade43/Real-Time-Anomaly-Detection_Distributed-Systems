docker run -d -p 3306:3306 --name db-mysql -e MYSQL_ROOT_PASSWORD="root" -e MYSQL_DATABASE="abnormal_db" -v $PWD/abnormal.sql:/docker-entrypoint-initdb.d/abnormal.sql --network ads_network mysql --default-authentication-plugin=mysql_native_password


docker run --name db-postgres -e POSTGRES_PASSWORD=root -p 5433:5432 -v /Users/stevemendis/Desktop/ADS_Final/db/abnormal.sql:/docker-entrypoint-initdb.d/abnormal.sql -d --network ads_network postgres:latest
