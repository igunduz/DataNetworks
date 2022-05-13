# 
# Import socket library and Hash(MD5) library
#
import socket
import hashlib
import os
#
# Generate md5 hash function
#
def generate_md5_hash (file_data):
    file_data = file_data.encode()
    md5_hash = hashlib.md5(file_data)
    f_id = md5_hash.hexdigest()
    return str(f_id)

def md5_check(md5_client,md5_server):
  if md5_client == md5_server:
    msg = "Success"
  else: msg = "Fail"
  return msg
# 
# Define Server URL and PORT
#
serverPort = 7700
serverURL = "localhost"
i = 0
# the name of file 
filename = "The_file.gif"
# get the file size
filesize = os.path.getsize(filename)

# Create TCP socket for future connections
clientSocket = socket.socket()
  
# Connect the client to the specified server#
clientSocket.connect((serverURL, serverPort))
print("Client connected to server: " + serverURL + ":" + str(serverPort))
  
# This client implements the following scenario:
# 1. SHOW_FILES
clientSocket.send("SHOW_FILES".encode())
# Receive data from server
dataFromServer = clientSocket.recv(1024)
# Print to the console
print(dataFromServer.decode())
  
# 2a. UPLOAD the specified file
if dataFromServer == b'No files available at the moment':
  clientSocket.send("UPLOAD".encode())
  # Receive data from server
  dataFromServer = clientSocket.recv(1024)
  clientSocket.send(str(filename+";"+str(filesize)).encode())
  # start sending the file
  with open(filename, "rb") as f:
    while True:
      bytes_read = f.read(1024)
      if not bytes_read:
            break
      clientSocket.sendall(bytes_read)
  # 2b. Check MD5
  md5_server = clientSocket.recv(1024)
  md5_client = generate_md5_hash(filename)
  check_Res = md5_check(md5_client,md5_server)
  print(check_Res)
    
# 3. SHOW_FILES
clientSocket.send("SHOW_FILES".encode())
# Receive data from server
answer = clientSocket.recv(1024).decode()
# Print to the console
print(answer)

# 4a. DOWNLOAD the previously uploaded file
if str(filename+";"+str(filesize)) in answer:
  #save the file_id
  file_id = answer.replace(str(filename+";"+str(filesize)),"")
  file_id = file_id.replace(";","")
#Send DOWNLOAD command to the server
clientSocket.send("DOWNLOAD".encode())
  
# Receive data from server Print to the console
#print(clientSocket.recv(1024).decode())

#Send the file_id to the server
clientSocket.send(file_id.encode())
  
# 4b. Check MD5
md5_server = clientSocket.recv(1024)
md5_client = generate_md5_hash(filename)
md5_check(md5_client,md5_server)
check_Res = md5_check(md5_client,md5_server)
print(check_Res)

#close TCP connection
clientSocket.close()
