'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''

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

    uploadedFile = None

    if uploadOption == "Text":

        # show the upload button for text files

    elif uploadOption == "Audio":

        # show the upload button for audio files

    elif uploadOption == "Video":

        # show the upload button for video files


    # if the file was uploaded in any of the three formats
    if uploadedFile is not None:

        fileBytes = uploadedFile.getvalue()
        fileSize = len(fileBytes)
    
        if st.button("Upload to Server"):

            # code that corresponds to sending commands and receiving responses
            # Option to overwrite the current file should be implemeneted as well
            # If the file already exists


# ======== DOWNLOAD ========
elif choice == "Download":

    st.header("Download Files")

    filename = st.text_input("Enter the filename to download:")

    if st.button("Request File"):

        # code that corresponds to sending commands and receiving responses



# ======== DELETE ========
elif choice == "Delete":

    st.header("Delete Files")


    if st.button("Delete File"):

        # code that corresponds to sending commands and receiving responses


# ======== DIR ========
elif choice == "Dir":

    st.header("View Directory (Files and Subdirectories)")

    if st.button("Refresh Directory"):

        # code that corresponds to sending commands and receiving responses

# ======== SUBFOLDER ========
elif choice == "Subfolder":

    st.header("Subfolder Creation & Deletion")

    action = st.radio(
        "Select Action for Subfolder", 
        ["Create", "Delete"],
        captions=[
            "(Creates subfolder in the server's file storage path)",
            "(Deletes subfolder in the server's file storage path)",
        ],

        index=None,
    )

    st.write("You Selected:", action)

    folderPath = st.text_input("Subfolder Path/Name")

    if st.button("Submit"):

        # code that corresponds to sending commands and receiving responses

