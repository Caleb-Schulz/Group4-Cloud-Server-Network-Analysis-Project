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
# 2) Then, 'streamlit run app.py --server.address 0.0.0.0 --server.port 5000'

import streamlit as st
import socket
import os
import threading
import sys
import hashlib

# -------- CONFIGURATION (Network Connection & Logics) --------

HOST = '0.0.0.0'  # Listens on all network interfaces
PORT = 5000       # Project port (The firewall rules have this port open)
BUFFER_SIZE = 4096

# -------- ESTABLISHING A CONNECTION --------

# working on it 

# -------- STREAMLIT UI --------

st.title("Cloud Server File Request & Transfer") # Title for the application

st.sidebar.header("Navigation") # Makes a clickable sidebar "Navigation"

menu = ["Connect", "Upload", "Download", "Delete", "Dir", "Subfolder"] # Array of File Operations

choice = st.sidebar.selectbox("Select Action", menu) # Selectable File Opeations

# ---- CONNECT ----

# -- AUTHENTICATION --

# wip ^^'

# ---- UPLOAD ----



# ---- DOWNLOAD ----



# ---- DELETE ----



# ---- DIR ----



# ---- SUBFOLDER ----




