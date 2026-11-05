import socket
import threading
import sys
import os

# Server Configuration
HOST = '0.0.0.0'  # Listens on all network interfaces
PORT = 5000       # Project port (The firewall rules have this port open)
BUFFER_SIZE = 4096

def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to Bind the socket to host and port
    try:
        server_socket.bind((HOST, PORT))
        print(f"Test: Server successfully bound to {HOST}:{PORT}") # Temp test
    except Exception as e: # Gracefully handle errors
        print(f"Error Failed to bind server: {e}") 
        sys.exit(1)

    # Temp end for test
    server_socket.close()

# The Start Function
if __name__ == "__main__":
    start_server()