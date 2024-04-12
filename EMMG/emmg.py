#from Crypto.Cipher import AES
from datetime import datetime
from confluent_kafka import Consumer, KafkaException, KafkaError
import mysql.connector
import pyaes
import base64
import os



conf = {
    'bootstrap.servers': 'mycas-kafka-service:9092',
    'group.id': 'emmg',
    'auto.offset.reset': 'earliest'
}

mysql_host = 'mycas-mysql-service'
mysql_user = 'omi_user'
mysql_password = 'omi_user'
mysql_database = 'cas'

# Create Kafka consumer
consumer = Consumer(conf)

# Subscribe to the topic
topic = 'topic_mycas'
consumer.subscribe([topic])

mysql_connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)
mysql_cursor = mysql_connection.cursor()

key = 'qwertyuioplkjhgd'
def encrypt_string(key, plaintext):
    block_size = 16

    # Generate a random initialization vector (IV)
    iv = pyaes.Counter(initial_value=0)

    # Create an AES cipher object with the provided key and CTR mode
    cipher = pyaes.AESModeOfOperationCTR(key.encode('utf-8'), counter=iv)

    # Pad the plaintext to a multiple of the block size
    padding_length = block_size - (len(plaintext) % block_size)
    padded_plaintext = plaintext + padding_length * chr(padding_length)

    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext.encode('utf-8'))

    # Encode the ciphertext in base64 for representation
    encrypted_data = base64.b64encode(ciphertext).decode('utf-8')

    return encrypted_data


try:
    while True:
        # Poll for messages
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        elif msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Reached end of partition, continue to next partition
                continue
            else:
                # Handle other errors
                print(f"Error: {msg.error().str()}")
                break
        else:
            # Process the message
            #encrypted_data = encrypt_message(msg.value(), aes_key, aes_iv)
            encrypted_data = encrypt_string(key, msg.value().decode('utf-8'))
            start_time = int(datetime.now().timestamp())

            # Parse the last column of the message to extract the date
            last_column = msg.value().decode('utf-8').split(':')[-1].strip()
            date_obj = datetime.strptime(last_column, '%Y-%m-%d')
            end_time = int(date_obj.replace(hour=0, minute=0, second=0).timestamp())
            emmtype = msg.value().decode('utf-8').split(':')[-2].strip()
            # Save the encrypted data, start time, end time, and other required information to the database
            insert_query = "INSERT INTO emmg (starttime, endtime, emmdata, emmtype) VALUES (%s, %s, %s, %s)"
            data = (start_time, end_time, encrypted_data, emmtype)
            mysql_cursor.execute(insert_query, data)
            mysql_connection.commit()
            mysql_cursor.close()
            mysql_connection.close()

except KeyboardInterrupt:
    # Stop consuming when interrupted
    pass

finally:
    # Close the consumer and MySQL connection to release resources
    consumer.close()
    mysql_cursor.close()
    mysql_connection.close()


