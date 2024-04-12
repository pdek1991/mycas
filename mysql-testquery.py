import mysql.connector.pooling

db_config = {
    "host": "mycas-mysql-service",
    "user": "test",
    "password": "test",
	"auth_plugin": "caching_sha2_password"
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=5, **db_config)

connection = connection_pool.get_connection()

cursor = connection.cursor()
insert_query = "use test;"
cursor.execute(insert_query)

insert_query = "CREATE TABLE entitlements (device_id VARCHAR(255), package_id VARCHAR(255),  expiry DATE);"
cursor.execute(insert_query)
connection.commit() 