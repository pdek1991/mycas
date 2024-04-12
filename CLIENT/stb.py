import socket
import struct
import sys
import pyaes
import base64
import time
#import tkinter as tk
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client import push_to_gateway
import os
# Define the multicast group and port
multicast_group = 'mycas-stb-service'
port = 1234
key = 'qwertyuioplkjhgd'
start_time = time.time()
total_bytes = 0
registry = CollectorRegistry()
emmbw = Gauge('mycas_emmbw', 'EMM BW in Kbps', registry=registry)
pushgateway_url = 'http://prometheus-pushgateway:9091'
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific interface and port
sock.bind(('', port))

# Join the multicast group
#group = socket.inet_aton(multicast_group)
#mreq = struct.pack('4sL', group, socket.INADDR_ANY)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Create an AES cipher object with the provided key and CTR mode
def decrypt_string(key, encrypted_data):
    block_size = 16

    # Generate the same initialization vector (IV) used during encryption
    iv = pyaes.Counter(initial_value=0)

    # Create an AES cipher object with the provided key and CTR mode
    cipher = pyaes.AESModeOfOperationCTR(key.encode('utf-8'), counter=iv)

    # Decode the base64-encoded ciphertext
    ciphertext = base64.b64decode(encrypted_data)

    # Decrypt the ciphertext
    padded_plaintext = cipher.decrypt(ciphertext).decode('utf-8')

    # Remove the padding from the plaintext
    padding_length = ord(padded_plaintext[-1])
    plaintext = padded_plaintext[:-padding_length]
    return plaintext

# Create a Tkinter window
#window = tk.Tk()
#window.title("STB")
#window.geometry("300x100")  # Set the window size

# Create a label to display the received data
#data_label = tk.Label(window, text="")
#data_label.pack()

# Function to update the label text with received data
def update_data_label(text):
    columns = text.split(':')
    if columns[0] == '7010000013' and columns[3] == '44':
        # Display the 2nd column on the GUI
        #message_label.config(text=columns[2])
        print(columns[2])
        
        
    else:
        print('error')
        #message_label.config(text="error")
    

    # Update the Tkinter event loop
    #window.update()
    
# Function to start receiving data
def start_receiving():
    global total_bytes
    global start_time
    try:
        while True:
            # Receive and process data from the multicast stream
            data, address = sock.recvfrom(1024)
            plaintext = decrypt_string(key, data)
            #print(f"Received data: {plaintext}")
            total_bytes += len(data)
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= 30:
                # Calculate bytes per second
                bytes_per_sec = (total_bytes / elapsed_time)/1024
                # Print the result
                print("BW in Kb:", bytes_per_sec)
                emmbw.set(bytes_per_sec)
                push_to_gateway(pushgateway_url, job='emmbw', registry=registry)
                # Reset counters and start time
                total_bytes = 0
                start_time = time.time()
            
            # Update the label in the GUI with received data
            #window.after(0, update_data_label, plaintext)
            
            columns = plaintext.split(':')
            if columns[0] == '7010000013' and columns[3] == '44':
                # Display the 2nd column on the GUI
                #message_label.config(text=columns[2])
                print(columns[2])
                #window.update()
            #update_data_label(plaintext)
            # Update the Tkinter event loop
            #window.update()
            
    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        #end_time = time.time()
        #elapsed_time = end_time - start_time
        # Calculate bytes per second
        #bytes_per_sec = total_bytes / elapsed_time
        # Print the final result
        #print("BW in Kb:", bytes_per_sec/1024)
        print("KeyboardInterrupt: Closing socket.")
        sock.close()
        sys.exit(0)

# Create a label to display the filtered data
#message_label = tk.Label(window, text="")
#message_label.pack()

# Start receiving data
start_receiving()

# Run the Tkinter event loop
#window.mainloop()
