#handle file upload, download, directory operations
#provide feedback to user based on status of file transfer and operations
#file operations: connect server IP port (initiates connection from client to server with 
#SPECIFIED FILES) [needs authentication], Upload[filename], download[filename], 
#delete a file, dir, view list of files and subdirectories in server file storage path
#subfolder, (create/delete) path/directory, clients can create or delete subfolders
#in server's file storage path

#how to compile: python -m py_compile [filename.py]
#how to run: python3 [filename].py

print("Which operation do you want to perform?\n")

print("Enter 1 for Upload")
print("Enter 2 for Download")
print("Enter 3 for Delete")
print("Enter 4 for View Directory")
print("Enter 5 for Create subfolder")
print("Enter 6 for Delete subfolder")

file_operation=input("Enter a choice: ")


def chooseFileOperation(file_operation):
#if file operation number invalid print a statement
#make user re-enter it again 
    if(file_operation > 6 or file_operation < 1):
        print("Invalid file operation. Please re-enter a valid number choice:\n")
        file_operation=input("Enter a choice: ")


#upload
def upload(file_operation):
    print("If you want to upload a file enter 1 and proceed to enter filename:")
    affirm_upload=input("")
