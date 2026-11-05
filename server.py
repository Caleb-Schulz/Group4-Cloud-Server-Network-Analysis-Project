import socket
import threading
import sys
import os

# Server Configuration
HOST = '0.0.0.0'  # Listens on all network interfaces
PORT = 5000       # Project port (The firewall rules have this port open)
BUFFER_SIZE = 4096

def handle_client(client_socket, address):
    # Handles the speration of client connections in to diffrent threads
    print(f"Handling client {address} in a new thread.")
    try:
        # here next
        pass
    finally:
        client_socket.close()
        print(f"Connection closed for {address}")

def start_server():
    # Create the TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow socket address to be reused
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Try to Bind the socket to host and port
    try:
        server_socket.bind((HOST, PORT))
    except Exception as e: # Gracefully handle errors
        print(f"Error Failed to bind server: {e}") 
        sys.exit(1)

    # listening for incoming connections
    server_socket.listen(5)
    print(f"Server is listening on port {PORT}... Press Ctrl+C to stop.")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection accepted from {address}")
            
            # Creates a new threads for each client so multiple clients can connect at once
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()

    # The Stop Function
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

# The Start Function
if __name__ == "__main__":
    start_server()