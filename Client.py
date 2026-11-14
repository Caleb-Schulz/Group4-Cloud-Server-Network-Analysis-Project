'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''
# =================================================================================================

# Note: Savitri and Kamini worked on this together.

# Anything that Kamini implemented & commented will be labeled with their name.
# If there is no name, those are Savitri's implementations & comments.

# Savitri worked with implementing & making the streamlit UI,
# along with establishing the connection & authentication process, all of the "CONNECT" operation
# and additional functions, such as the sendCommand

# Kamini worked on implementing the inner operational logics of the different operations
# "UPLOAD", "DOWNLOAD", "DELETE", "DIR", "SUBFOLDER"

# =================================================================================================


# to run type in terminal 'streamlit run Client.py'

# WILL NEED TESTING WHEN THIS PORTION IS DONE:

# On the Google Cloud VM Instance SSH, 
# 1) First install 'pip install streamlit'
# 2) Then, 'streamlit run Client.py --server.address 0.0.0.0 --server.port 8501'

import streamlit as st
import socket
import os
import hashlib

# ============ CONFIGURATION (Network Connection & Logics) ============

host = '136.115.113.19'  # Set to the Static GCP public IP address
port = 5000       # Project port (The firewall rules have this port open)
BUFFER_SIZE = 4096

# ======== Session State Check ========

# Needed to keep session state after every click
# Otherwise, each click would run the code from top to bottom

if "sock" not in st.session_state:
    st.session_state.sock = None

if "connected" not in st.session_state:
    st.session_state.connected = False

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ======== Additional Functions ========

# Hashes password for securtiy purposes
# Takes care of not transmitting the password in clear text
def hashPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest() # hashes the password

# Function to be reused for every file operation (command)
# Network sockets can't take string input, so makes it into bytes and sends
# Then it waits to recieve a response, with the buffer size reading at a time
# Returns the response
# If connection error occurs, it gets catched through except
# Updates the status displayed via sidebar

def sendCommand(command):
    try:
        st.session_state.sock.sendall((command + "\n").encode('utf-8'))
       
        response = st.session_state.sock.recv(BUFFER_SIZE).decode('utf-8').strip()
       
        return response

    except Exception as e:
        
        st.session_state.connected = False
        
        st.session_state.authenticated = False
        
        return f"ERROR: Connection Lost ({e})"

# ============ STREAMLIT UI ============

st.title("Cloud Server File Request & Transfer") # Title for the application

st.sidebar.header("Navigation") # Makes a clickable sidebar "Navigation"

menu = ["Connect", "Upload", "Download", "Delete", "Dir", "Subfolder"] # Array of File Operations

choice = st.sidebar.selectbox("Select Action", menu) # Selectable File Opeations


# ---- Status Indicator in Sidebar ----

if st.session_state.authenticated:
    st.sidebar.success("Status: Connected & Authenticated")

elif st.session_state.connected:
    st.sidebar.warning("Status: Connected (Not Authenticated)")

else:
    st.sidebar.error("Status: Disconnected")


# ======== CONNECT ========
if choice == "Connect":

    # Login screen to make a connection
    # Input different fields needed to make the connection
    # Typed user password is masked with dots for security

    st.header("Connect & Authenticate")

    serverIP = st.text_input("Server IP Address", value=host) # default value for testing

    serverPort = st.number_input("Server Port", value=port) # default value for testing

    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    # Making two columns to display "Connect" and "Disconnect" for user

    # col1 is for users to connect to the server:
    # If the user selects the "Connection Login" button,
    # it uses the previously inputted information
    # to create a connection with the server with socket
    # and sets the connection variable to "True"
    # If it succeeds (known from the response after sending user & pass),
    # it sets the authentication variables to "True"
    # If no connection was made, it will send an error message
    

    # col2 is for users to disconnect from the server:
    # If the user selects the "Disconnect" button,
    # it closes the connection socket
    # and sets the connection & authentication variables to "False"

    col1, col2 = st.columns(2)

    with col1:
        
        if st.button("Connection Login"):
            try:
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((serverIP, int(serverPort)))
                st.session_state.sock = s
                st.session_state.connected = True

                greeting = s.recv(BUFFER_SIZE).decode('utf-8').strip()

                hashed_password = hashPassword(password)
                authRESP = sendCommand(f"{username}:{hashed_password}")

                if "SUCCESS" in authRESP:

                    st.session_state.authenticated = True
                    st.success("Connected and Authenticated Successfully.")

                else:
                    st.error(f"Authentication Failed: {authRESP}")
                    s.close()
                    st.session_state.sock = None
                    st.session_state.connected = False
            
            except Exception as e:
                st.error(f"Failed to Connect: {e}")
    
    with col2:

        if st.button("Disconnect"):

            if st.session_state.sock:
                st.session_state.sock.close()

            st.session_state.sock = None
            st.session_state.connected = False
            st.session_state.authenticated = False

            st.info("Disconnrcted From Server.")


# Last part to guard the file operations
# If connection is not authenticated, user will have to go login

elif not st.session_state.authenticated:
    st.warning("Please go to 'Connection Login' and log into the server first.")


# ======== UPLOAD ========
elif choice == "Upload":

    st.header("Upload Files")

    # User gets to select the type of file they want to upload
    # Supports text, audio and video file

    uploadOption = st.radio(
        "Select File Type", 
        ["Text", "Audio", "Video"],
        captions=[
            "(.txt)",
            "(.mp3)",
            "(.mp4)",
        ],

        index=None,
    )

    st.write("You Selected:", uploadOption)

    filename = None

    # Upload type chosen based on user's answer

    if uploadOption == "Text":
        
        # Kamini - show the upload button for text files
        filename = st.file_uploader("Choose a file: ", type="txt", max_upload_size=100000)

    elif uploadOption == "Audio":

        # Kamini - show the upload button for audio files
        filename = st.file_uploader("Choose a file: ", type="mp3", max_upload_size=100000)

    elif uploadOption == "Video":

        # Kamini - show the upload button for video files
        filename = st.file_uploader("Choose a file: ", type="mp4", max_upload_size=100000)


    # Kamini - if the file was uploaded in any of the three formats
    if filename is not None:

        # Kamini - First convert the file into bytes so that the computer can read it
        byte_data = filename.getvalue()
    
        if st.button("Upload to Server"):
          
            try: 
                # code that corresponds to sending commands and receiving responses
               
                # Kamini - Next, process the uploaded file:
                # Kamini - uploadRESP is the variable which holds the result of the server's response to the UPLOAD command
                uploadRESP = sendCommand(f"UPLOAD {filename.name}")

                # Kamini -check for filename provided:
                if "Error: No filename provided" in uploadRESP:  
                    st.error("Please provide a filename.")

                # Server responds with "already exists"
                # So user needs to be asked wheter to overwrite next
                elif "File already exists" in uploadRESP:
                    st.session_state.ask_overwrite = True

                # Kamini - if file does not exist, we can readily upload it:
                elif "Ready, send file data" in uploadRESP:
                    st.session_state.sock.sendall(byte_data)
                    st.success("File Uploaded Successfully!")

                # If any other error occur
                else:
                    st.error(uploadRESP)

            except Exception as e:
            st.error(f"Error reading file: {e}")


        # Option to overwrite the current file should be implemeneted
        # If the file already exists
        if st.session_state.get("ask_overwrite"):
            
            overwrite = st.radio(
                "Overwrite existing file?", 
                    ["Yes", "No"],
                    index=None,
            )

            # Kamini - if client selects 'y', server response is ready, send file data
            if overwrite == "Yes":
                # Kamini - logic to send 'y' to server
                st.session_state.sock.sendall("y")

                st.session_state.sock.sendall(byte_data)
                st.success("File Uploaded Successfully!")
                

            # Kamini - if client selects 'n', server response is upload cancelled by user, and overwrite was cancelled:
            elif overwrite == "No":
                # Kamini - logic to send 'n' to server
                st.session_state.sock.sendall("n")
                response = st.session_state.sock.recv(BUFFER_SIZE).decode('utf-8') # Kamini - client receives the response from the server

                if "Upload cancelled by user" in response:
                    st.error("Upload Overwrite Cancelled.")
                
                st.session_state.ask_overwrite = False


    else:
        st.info("Please upload a file to proceed.")

# ======== DOWNLOAD ========
elif choice == "Download":

    st.header("Download Files")

    filename = st.text_input("Enter the filename to download:")

    if st.button("Request File"):
        pass  # Temp placeholder
        # code that corresponds to sending commands and receiving responses



# ======== DELETE ========
elif choice == "Delete":

    st.header("Delete Files")


    if st.button("Delete File"):
        pass  # Temp placeholder
        # code that corresponds to sending commands and receiving responses


# ======== DIR ========
elif choice == "Dir":

    st.header("View Directory (Files and Subdirectories)")

    if st.button("Refresh Directory"):
        pass  # Temp placeholder
        # code that corresponds to sending commands and receiving responses

# ======== SUBFOLDER ========
elif choice == "Subfolder":

    st.header("Subfolder Creation & Deletion")

    action = st.radio(
        "Select Action for Subfolder", 
        ["create", "delete"],
        captions=[
            "(Creates subfolder in the server's file storage path)",
            "(Deletes subfolder in the server's file storage path)",
        ],

        index=None,
    )

    st.write("You Selected:", action)

    folderPath = st.text_input("Subfolder Path/Name")

    if st.button("Submit"):
        pass  # Temp placeholder
        # code that corresponds to sending commands and receiving responses

