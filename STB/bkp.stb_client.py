import socket
import struct
import sys
import pyaes
import base64
import time
import tkinter as tk
# Define the multicast group and port
multicast_group = '224.1.1.1'
port = 5000
key = 'qwertyuioplkjhgd'
start_time = time.time()
total_bytes = 0

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific interface and port
sock.bind(('', port))

# Join the multicast group
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

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

try:
    while True:
        # Receive and process data from the multicast stream
        data, address = sock.recvfrom(1024)
        plaintext = decrypt_string(key, data)
        print(f"Received data: {plaintext}")
        total_bytes += len(data)
        
        elapsed_time = time.time() - start_time
        if elapsed_time >= 30:
            # Calculate bytes per second
            bytes_per_sec = total_bytes / elapsed_time
            # Print the result
            print("BW in Kb:", bytes_per_sec/1024)
            # Reset counters and start time
            total_bytes = 0
            start_time = time.time()
            
except KeyboardInterrupt:
    # Handle Ctrl+C interruption
    end_time = time.time()
    elapsed_time = end_time - start_time
    # Calculate bytes per second
    bytes_per_sec = total_bytes / elapsed_time
    # Print the final result
    print("BW in Kb:", bytes_per_sec/1024)
    print("KeyboardInterrupt: Closing socket.")
    sock.close()
    sys.exit(0)
