import streamlit as st
import pandas as pd 
from io import StringIO
import socket
import os 
import requests


#handle file upload, download, directory operations
#provide feedback to user based on status of file transfer and operations
#file operations: connect server IP port (initiates connection from client to server with 
#SPECIFIED FILES) [needs authentication], Upload[filename], download[filename], 
#delete a file, dir, view list of files and subdirectories in server file storage path
#subfolder, (create/delete) path/directory, clients can create or delete subfolders
#in server's file storage path

#how to compile: python -m py_compile [filename.py]
#how to run: python3 [filename].py

#streamlit run [Filename].py


#file operations:

#Upload: [1==Text, 2==Audio, 3==Video]

#Download: [4==Text, 5==Audio, 6==Video]

#delete: [7==Text, 8==Audio, 9==Video]

#view directory: [10==view directory]

#create new subfolder: [11== create new subfolder]

#delete existing subfolder: [12== delete existing subfolder]

"""
print("Choose a file operation you want to perform\n")

print("Enter 1 for Upload Text File")
print("Enter 2 for Upload Audio File")
print("Enter 3 for Upload Video File")
print("Enter 4 for Download Text File")
print("Enter 5 for Download Audio File")
print("Enter 6 for Download Video File")
print("Enter 7 for Delete Text File")
print("Enter 8 for Delete Audio File")
print("Enter 9 for Delete Video File")
print("Enter 10 to View Directory")
print("Enter 11 to Create a New Subfolder")
print("Enter 12 to Delete an Existing Subfolder")

file_operation=int(input("Enter a choice: "))


#if statement: file operation number invalid print a statement
#make user re-enter it again
if file_operation > 12 or file_operation < 1:
    print("Invalid file operation. Please re-enter a valid number choice:\n")
    file_operation=int(input("Enter a choice "))

if file_operation == 1:
"""
# You Should use the stream lit build in features to make the GUI instead of text menu system

st.header("Upload Text File")

# type should be a list of strings, and removed invalid max_upload_size parameter
upload_file = st.file_uploader("Choose a file:", type=["txt"])

if upload_file is not None:
    # First convert the file into bytes so that the computer can read it
    byte_data = upload_file.getvalue()

    # Next, process the uploaded file:
    try:
        # check upload_file.name
        if upload_file.name.endswith(".txt"):
            st.success(f"TXT file '{upload_file.name}' uploaded successfully!")
            
            # Here is where you would call their socket send logic
        else:
            st.error("Unsupported file type.")
    
    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("Please upload a file to proceed.")