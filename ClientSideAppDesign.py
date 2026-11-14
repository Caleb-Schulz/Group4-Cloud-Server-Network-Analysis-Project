import streamlit as st
import socket
import os 
import requests


#handle file upload, download, directory operations
#provide feedback to user based on status of file transfer and operations
#file operations: connect server IP port (initiates connection from client to server with 
#SPECIFIED FILES) [needs authentication]
#file operations (my end): Upload[filename], download[filename], delete [filename], view dir [list of files & subdir in server file storage path]
#create/delete subfolders

#how to compile: python -m py_compile [filename.py]
#how to run: python3 [filename].py

#streamlit run [Filename].py


#file operations:

#Upload: [1==Text, 2==Audio, 3==Video]

#Download: [4==Text, 5==Audio, 6==Video]

#Delete: [7==Text, 8==Audio, 9==Video]

#view directory: [10==view directory]

#Create new subfolder: [11== create new subfolder]

#Delete existing subfolder: [12== delete existing subfolder]


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


#if statement: file operation number invalid, make user re-enter file_operation choice again
if file_operation > 12 or file_operation < 1:

    while file_operation > 12 or file_operation < 1:
        print("\nInvalid file operation. Please re-enter a valid number choice:")
        file_operation=int(input("Enter a choice "))




#=================================================[OPTION 1 UPLOAD TEXT FILE]:===================================================
if file_operation == 1:
    filename = st.file_uploader("Choose a file: ", type=txt, max_upload_size=100000)

    #First convert the file into bytes so that the computer can read it
    if filename is not None:
        byte_data = upload_file.getvalue()

        #Next, process the uploaded file:
        try:
            #uploadRESP is the variable which holds the result of the server's response to the UPLOAD command
            uploadRESP = sendCommand(f"UPLOAD_RESPONSE: {filename}")

            #check for filename provided:
            if "Error: No filename provided" in uploadRESP:  
                st.error("Please provide a filename.")

            #check if file already exists:
            elif "File already exists" in uploadRESP:
                print("Do you want to Overwrite this file? Y/N?")
                choice=input("Y/N?")                                #create choice variable for client
                st.session_state.sock.sendall(choice)               #client sends the choice to the server
                
                #if client selects 'N', server response is upload cancelled by user, and overwrite was cancelled:
                response = st.session_state.sock.recv(BUFFER_SIZE).decode('utf-8') #client receives the response from the server
                if "Upload cancelled by user" in response:
                    st.error("Upload Overwrite Cancelled.")
                
                else: #if client selects 'Y', server response is ready, send file data:
                    st.session_state.sock.sendall(byte_data)
                    st.success("File Uploaded Successfully!")

            #if file does not exist, we can readily upload it:
            elif "Ready, send file data" in uploadRESP:
                st.session_state.sock.sendall(byte_data)
                st.success("File Uploaded Successfully!")


        except Exception as e:
            st.error(f"Error reading file:" {e})
    
    else:
        st.info("Please upload a file to proceed.")




#===================================================[OPTION 2 UPLOAD AUDIO FILE]:===================================================
if file_operation == 2:
    filename = st.file_uploader("Choose a file: ", type=mp3, max_upload_size=100000)

    #First convert the file into bytes so that the computer can read it
    if filename is not None:
        byte_data = upload_file.getvalue()

        #Next, process the uploaded file:
        try:
            #uploadRESP is the variable which holds the result of the server's response to the UPLOAD command
            uploadRESP = sendCommand(f"UPLOAD_RESPONSE: {filename}")

            #check for filename provided:
            if "Error: No filename provided" in uploadRESP:  
                st.error("Please provide a filename.")

            #check if file already exists:
            elif "File already exists" in uploadRESP:
                print("Do you want to Overwrite this file? Y/N?")
                choice=input("Y/N?")                                #create choice variable for client
                st.session_state.sock.sendall(choice)               #client sends the choice to the server
                
                #if client selects 'N', server response is upload cancelled by user, and overwrite was cancelled:
                response = st.session_state.sock.recv(BUFFER_SIZE).decode('utf-8') #client receives the response from the server
                if "Upload cancelled by user" in response:
                    st.error("Upload Overwrite Cancelled.")
                
                else: #if client selects 'Y', server response is ready, send file data:
                    st.session_state.sock.sendall(byte_data)
                    st.success("File Uploaded Successfully!")

            #if file does not exist, we can readily upload it:
            elif "Ready, send file data" in uploadRESP:
                st.session_state.sock.sendall(byte_data)
                st.success("File Uploaded Successfully!")


        except Exception as e:
            st.error(f"Error reading file:" {e})
    
    else:
        st.info("Please upload a file to proceed.")





#================================================[OPTION 3 UPLOAD VIDEO FILE]:===================================================
if file_operation == 3:
    filename = st.file_uploader("Choose a file: ", type=mp4, max_upload_size=100000)

    #First convert the file into bytes so that the computer can read it
    if filename is not None:
        byte_data = upload_file.getvalue()

        #Next, process the uploaded file:
        try:
            #uploadRESP is the variable which holds the result of the server's response to the UPLOAD command
            uploadRESP = sendCommand(f"UPLOAD_RESPONSE: {filename}")

            #check for filename provided:
            if "Error: No filename provided" in uploadRESP:  
                st.error("Please provide a filename.")

            #check if file already exists:
            elif "File already exists" in uploadRESP:
                print("Do you want to Overwrite this file? Y/N?")
                choice=input("Y/N?")                                #create choice variable for client
                st.session_state.sock.sendall(choice)               #client sends the choice to the server
                
                #if client selects 'N', server response is upload cancelled by user, and overwrite was cancelled:
                response = st.session_state.sock.recv(BUFFER_SIZE).decode('utf-8') #client receives the response from the server
                if "Upload cancelled by user" in response:
                    st.error("Upload Overwrite Cancelled.")
                
                else: #if client selects 'Y', server response is ready, send file data:
                    st.session_state.sock.sendall(byte_data)
                    st.success("File Uploaded Successfully!")

            #if file does not exist, we can readily upload it:
            elif "Ready, send file data" in uploadRESP:
                st.session_state.sock.sendall(byte_data)
                st.success("File Uploaded Successfully!")


        except Exception as e:
            st.error(f"Error reading file:" {e})
    
    else:
        st.info("Please upload a file to proceed.") 

