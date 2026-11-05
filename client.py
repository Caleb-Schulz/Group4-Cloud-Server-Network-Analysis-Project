"""
1. AUTHENTICATION HANDSHAKE (Required immediately upon connection):
   - Server sends: "AUTH_REQUIRED\n"
   - Client sends: "username:password\n" (Password hashed/checked server-side)
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