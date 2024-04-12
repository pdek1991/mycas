#STB:

import socket

# Define the listening address and port
LISTEN_ADDRESS = '0.0.0.0'  # Listen on all available interfaces
LISTEN_PORT = 8888

def receive_message():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the listening address and port
        s.bind((LISTEN_ADDRESS, LISTEN_PORT))
        # Start listening for incoming connections
        s.listen()
        # Accept a connection
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            # Receive data from the sender
            data = conn.recv(1024)
    return data.decode('utf-8')

# Example usage
if __name__ == "__main__":
    # Receiving a message
    received_message = receive_message()
    print("Received message:", received_message)




#CYCLER

import socket

# Define the address and port of the receiver pod
#RECEIVER_POD_IP = '10.244.189.108'  # Replace with the actual IP address of the receiver pod
RECEIVER_POD_IP = 'stb-service-tmp'
RECEIVER_PORT = 8888

def send_message(message):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the receiver pod
        s.connect((RECEIVER_POD_IP, RECEIVER_PORT))
        # Send the message
        s.sendall(message.encode('utf-8'))

# Example usage
if __name__ == "__main__":
    # Sending a message
    send_message("Hello from sender pod!")
