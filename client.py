"""
1. AUTHENTICATION HANDSHAKE (Required immediately upon connection):
   - Server sends: "AUTH_REQUIRED\n"
   - Client sends: "username:sha256_hash\n" (The password is hashed locally on the client side using SHA-256; the plaintext password never crosses the network)
   - Server responds: "SUCCESS: Authenticated\n" OR "ERROR: Authentication failed.\n"

2. COMMAND FORMATS (Sent as plain text strings ending with '\n' or commands):
   - DIR
     * Description: Lists all files in the server storage.
     * Response: "Files in storage -> file1.txt, file2.png\n"

   - UPLOAD [filename]
     * Description: Uploads a file to the server.
     * Flow: Sends command -> Server checks if file exists, prompts if overwrite -> Client sends 'y'/'n' -> Client sends file binary stream.

   - DOWNLOAD [filename]
     * Description: Downloads a file from the server.
     * Flow: Sends command -> Server replies with size -> Client reads binary stream.

   - DELETE [filename]
     * Description: Deletes a specified file from storage.
     * Response: "File '[filename]' deleted successfully.\n"

   - SUBFOLDER {create|delete} [path]
     * Description: Creates or deletes a nested folder within storage.
     * Response: "Subfolder '[path]' created/deleted successfully.\n"
"""

# This is an authentication test I made that runs from a local machine,
# It should make a good starting point, but feel free to change it
import socket
import hashlib

HOST = "136.115.113.19"  # GCP static IP
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Reads the server's greeting
greeting = client.recv(1024).decode().strip()
print("Server greeting:", greeting)

# Prompt user to enter credentials dynamically
username = input("Enter username: ").strip()
plaintext_password = input("Enter password: ").strip()

# Hash the password locally using SHA-256 (plaintext never touches the wire)
password_hash = hashlib.sha256(plaintext_password.encode('utf-8')).hexdigest()

# Send username and the SHA-256 hash separated by a colon
auth_payload = f"{username}:{password_hash}\n"
client.sendall(auth_payload.encode('utf-8'))

# Reads the server's response
response = client.recv(1024).decode().strip()
print("Auth Response:", response)

# Stops after Authentication
client.close()