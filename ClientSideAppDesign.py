#handle file upload, download, directory operations
#provide feedback to user based on status of file transfer and operations
#file operations: connect server IP port (initiates connection from client to server with 
#SPECIFIED FILES) [needs authentication], Upload[filename], download[filename], 
#delete a file, dir, view list of files and subdirectories in server file storage path
#subfolder, (create/delete) path/directory, clients can create or delete subfolders
#in server's file storage path

#how to compile: python -m py_compile [filename.py]
#how to run: python3 [filename].py

print("Choose a file operation you want to perform\n")

print("Enter 1 for Upload")
print("Enter 2 for Download")
print("Enter 3 for Delete")
print("Enter 4 for View Directory")
print("Enter 5 for Create subfolder")
print("Enter 6 for Delete subfolder")

file_operation=int(input("Enter a choice: "))


#if-statement file operation number invalid print a statement
#make user re-enter it again
if file_operation > 6 or file_operation < 1:
    print("Invalid file operation. Please re-enter a valid number choice:\n")
    file_operation=int(input("Enter a choice "))


#upload:
if file_operation == 1:
    print("you chose to upload")


#download:
elif file_operation == 2:
    print("you chose to download")

#delete:
elif file_operation == 3:
    print("you chose to delete")


#view directory:
elif file_operation == 4:
    print("you chose to view directory")


#create a new subfolder:
elif file_operation == 5:
    print("you chose to create a new subfolder")


#delete an existing subfolder:
elif file_operation == 6:
    print("you chose to delete an existing subfolder")

