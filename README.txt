#Create docker container for Mysql
docker run --name mycas_db -e MYSQL_ROOT_PASSWORD=pdek -d -p 3306:3306 pdek1991/mycas_mysql

sudo docker exec -it mycas_db mysql -h 127.0.0.1 -P 3306 -u root -p

CREATE DATABASE cas;
CREATE USER 'omi_user'@'%' IDENTIFIED BY 'omi_user';

create user 'test'@'%' IDENTIFIED with mysql_native_password by 'test';
GRANT ALL PRIVILEGES ON cas.* TO 'omi_user'@'%';
GRANT ALL PRIVILEGES ON test.* TO 'test'@'%';

FLUSH PRIVILEGES;

USE cas;

CREATE TABLE entitlements (
    device_id VARCHAR(255),
    package_id VARCHAR(255),
    expiry DATE
);

CREATE TABLE devices (
    device_id VARCHAR(255),
    bskeys VARCHAR(255)
);

CREATE TABLE generate_osm (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    message_text TEXT,  
    device_id VARCHAR(255),
    expiry DATE
);


CREATE TABLE emmg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    starttime INT,  
    endtime INT,    
    emmdata TEXT,   
    emmtype VARCHAR(255)
);



#Create kafka container and push

crete image fro dockerfile-kafka
sudo docker run -d --name mycas_kafka -p 9092:9092 -p 2181:2181 pdek1991/mycas_kafka

After deploying kafka change listener and advertised listeners to 0.0.0.0 and service name 
##Code changes

Modify code to communicate over service of producer
bootstrap_servers = 'kafka-service:9092'

db_config = {
    "host": "mysql-service",
    "user": "omi_user",
    "password": "omi_user",
    "database": "cas",
}


docker run -d --name mycas_webapp -p 8080:8080 pdek1991/mycas_webapp


##on Kubernetes cluster to run all pod
docker ps -a | grep -vi up | for i in `awk -F " " '{print $1}'`; do docker start $i; done


Update mysql-connector and use mysql_native_password