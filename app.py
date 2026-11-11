'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''

# to run type in terminal 'streamlit run app.py'

# WILL NEED TESTING WHEN THIS PORTION IS DONE:

# On the Google Cloud VM Instance SSH, 
# 1) First install 'pip install streamlit'
# 2) Then, 'streamlit run app.py --server.address 0.0.0.0 --server.port 8501'

import streamlit as st
import socket
import os
import threading
import sys
import hashlib

# ======== CONFIGURATION (Network Connection & Logics) ========

host = '0.0.0.0'  # Listens on all network interfaces
port = 5000       # Project port (The firewall rules have this port open)
BUFFER_SIZE = 4096

# -------- Session State Check --------

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
def hashPassword(password)
    return hashlib.sha256(password.encode('utf-8').hexdigest()) # hashes the password

# Function to be reused for every file operation (command)
# Network sockets can't take string input, so makes it into bytes and sends
# Then it waits to recieve a response, with the buffer size reading at a time
# Returns the response
# If connection error occurs, it gets catched through except
# Updates the status displayed via sidebar

def sendCommand(command)
   try:
        st.session_state.sock.sendall(command.encode('utf-8'))
       
        response = st.session_state.sock.recv(BUFFER_SIZE).decode('utf-8')
       
        return response

    except Exception as e:
        
        st.session_state.connected = False
        
        st.session_state.authenticated = False
        
        return f"ERROR: Connection Lost ({e})"


# ======== ESTABLISHING A CONNECTION ========

# working on it 

def send_request():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.connect((host, port))

# ======== STREAMLIT UI ========

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


# -------- CONNECT --------
if choice == "Connect"

# wip ^^'

# -------- UPLOAD --------
if choice == "Upload"



# -------- DOWNLOAD --------
if choice == "Download"



# -------- DELETE --------
if choice == "Delete"



# -------- DIR --------
if choice == "Dir"



# -------- SUBFOLDER --------
if choice == "Subfolder"




