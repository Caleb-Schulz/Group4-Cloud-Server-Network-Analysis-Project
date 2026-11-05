import socket
import threading
import sys
import os
import hashlib

# Server Configuration
HOST = '0.0.0.0'  # Listens on all network interfaces
PORT = 5000       # Project port (The firewall rules have this port open)
BUFFER_SIZE = 4096

# Create the dedicated storage directory
STORAGE_DIR = os.path.join(os.getcwd(), "server_storage")
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def authenticate_client(auth_data):
    # Verifies client credentials against environment variables

    expected_user = os.getenv("SERVER_USER", "admin")
    expected_pass_hash = os.getenv("SERVER_PASS_HASH", hashlib.sha256("securepassword123".encode()).hexdigest())
    
    try:
        parts = auth_data.split(':', 1)
        if len(parts) != 2:
            return False
        user, password = parts[0], parts[1]
        
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        return user == expected_user and pass_hash == expected_pass_hash
    except Exception:
        return False

def handle_client(client_socket, address):
    # Handles the speration of client connections in to diffrent threads
    print(f"Handling client {address} in a new thread.")
    try:
        # Require authentication before allowing any commands
        client_socket.sendall(b"AUTH_REQUIRED\n")
        auth_data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
        
        # Verify credentials against environment variables
        if not authenticate_client(auth_data):
            client_socket.sendall(b"ERROR: Authentication failed.\n")
            return # Drop connection
            
        client_socket.sendall(b"SUCCESS: Authenticated\n")
        
        while True:
            # Get data from the client socket 
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break # Client disconnected
                
            message = data.decode('utf-8').strip()
            print(f"[{address}] Received: {message}")
            
            # Simple command parsing
            parts = message.split(' ', 1)
            command = parts[0].upper()
            args = parts[1] if len(parts) > 1 else ""
            
            # Route the commands
            if command == "DIR":
                try:
                    files = os.listdir(STORAGE_DIR)
                    if files:
                        file_list = ", ".join(files)
                        response = f"Files in storage -> {file_list}\n"
                    else:
                        response = "Storage directory is empty.\n"
                except Exception as e:
                    response = f"Error: Could not list directory -> {e}\n"

            elif command == "UPLOAD":
                filename = args.strip()
                if not filename:
                    response = "Error: No filename provided.\n"
                    client_socket.sendall(response.encode('utf-8'))
                    continue
                    
                file_path = os.path.join(STORAGE_DIR, filename)
                
                # Check if file already exists
                if os.path.exists(file_path):
                    client_socket.sendall(b"File already exists. Overwrite? (y/n): ")
                    choice = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip().lower()
                    if choice != 'y':
                        client_socket.sendall(b"Upload cancelled by user.\n")
                        continue
                
                # Tell the client we are ready to receive the file
                client_socket.sendall(b"Ready, send file data\n")
                
                try:
                    # Receive and save the file data
                    with open(file_path, 'wb') as f:
                        client_socket.settimeout(2.0) 
                        while True:
                            try:
                                chunk = client_socket.recv(BUFFER_SIZE)
                                if not chunk:
                                    break
                                f.write(chunk)
                            except socket.timeout:
                                break
                    client_socket.settimeout(None) 
                    response = f"File '{filename}' uploaded successfully.\n"
                except Exception as e:
                    response = f"Error:Failed to save file -> {e}\n"

            elif command == "DOWNLOAD":
                filename = args.strip()
                if not filename:
                    response = "No filename provided.\n"
                    client_socket.sendall(response.encode('utf-8'))
                    continue
                    
                file_path = os.path.join(STORAGE_DIR, filename)
                
                # Check if file exists on the server
                if not os.path.exists(file_path) or not os.path.isfile(file_path):
                    response = f"Error: File '{filename}' does not exist.\n"
                    client_socket.sendall(response.encode('utf-8'))
                else:
                    try:
                        file_size = os.path.getsize(file_path)
                        # Signal ready and send file size info
                        client_socket.sendall(f"Sending file ({file_size} bytes)\n".encode('utf-8'))
                        
                        # Open and stream the file data in chunks
                        with open(file_path, 'rb') as f:
                            while True:
                                chunk = f.read(BUFFER_SIZE)
                                if not chunk:
                                    break
                                client_socket.sendall(chunk)
                                
                        print(f"[{address}] Successfully sent file: {filename}")
                    except Exception as e:
                        response = f"Error: Failed to send file -> {e}\n"
                        client_socket.sendall(response.encode('utf-8'))

            elif command == "DELETE":
                filename = args.strip()
                if not filename:
                    response = "Error: No filename provided.\n"
                    client_socket.sendall(response.encode('utf-8'))
                    continue
                    
                file_path = os.path.join(STORAGE_DIR, filename)
                
                # Check if file exists
                if not os.path.exists(file_path) or not os.path.isfile(file_path):
                    response = f"Error: File '{filename}' does not exist.\n"
                else:
                    try:
                        # Try to delete the file
                        os.remove(file_path)
                        response = f"File '{filename}' deleted successfully.\n"
                        print(f"[{address}] Successfully deleted file: {filename}")
                    except PermissionError:
                        response = f"Error: File '{filename}' is currently being processed or locked.\n"
                    except Exception as e:
                        response = f"Error: Failed to delete file -> {e}\n"

            elif command == "SUBFOLDER":
                sub_parts = args.split(' ', 1)
                action = sub_parts[0].lower() if len(sub_parts) > 0 else ""
                subpath = sub_parts[1].strip() if len(sub_parts) > 1 else ""
                
                if not action or not subpath:
                    response = "Error: Invalid syntax. Use 'SUBFOLDER {create|delete} <path>'\n"
                else:
                    target_dir = os.path.abspath(os.path.join(STORAGE_DIR, subpath))
                    
                    # Ensure target stays inside STORAGE_DIR
                    if not target_dir.startswith(os.path.abspath(STORAGE_DIR)):
                        response = "Error: Invalid path outside storage directory.\n"
                    elif action == "create":
                        try:
                            os.makedirs(target_dir, exist_ok=True)
                            response = f"Subfolder '{subpath}' created successfully.\n"
                            print(f"[{address}] Successfully created subfolder: {subpath}")
                        except Exception as e:
                            response = f"Error: Failed to create subfolder -> {e}\n"
                    elif action == "delete":
                        try:
                            if os.path.exists(target_dir) and os.path.isdir(target_dir):
                                os.rmdir(target_dir)
                                response = f"Subfolder '{subpath}' deleted successfully.\n"
                                print(f"[{address}] Successfully deleted subfolder: {subpath}")
                            else:
                                response = f"Error: Subfolder '{subpath}' does not exist.\n"
                        except OSError:
                            response = f"Error: Subfolder '{subpath}' is not empty or cannot be removed.\n"
                        except Exception as e:
                            response = f"Error: Failed to delete subfolder -> {e}\n"
                    else:
                        response = f"Error: Unknown subfolder action '{action}'. Use 'create' or 'delete'.\n"

            else: # Gracefully handle errors
                response = f"ERROR: Unknown command '{command}'\n"
                
            client_socket.sendall(response.encode('utf-8'))
        
    except ConnectionResetError: # Gracefully handle errors
        print(f"Error: Client {address} abruptly disconnected.")
        
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
    except Exception as e:
        print(f"Error: Failed to bind server: {e}") 
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