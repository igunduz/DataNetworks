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
# 
# Define Server URL and PORT
#
serverPort = 7700
serverURL = "localhost"
# 
# Create TCP socket for future connections
#
serverSocket = socket.socket()
# 
# Bind URL and Port to the created socket
#
serverSocket.bind((serverURL, serverPort))
# 
# Start listening for incoming connection (1 client at a time)
#
serverSocket.listen(1)
print("Server is listening on port: " + str(serverPort))

while True:
    # 
    # Accept incoming client connection
    #
    connectSocket, addr = serverSocket.accept()
    print("Client connected: " + str(addr))
    
    #recieve command from the client
    request = connectSocket.recv(1024).decode()
    
    if request == "SHOW_FILES":
        if os.path.getsize('.') == 0:
            connectSocket.send("No files available at the moment".encode())
            break
        else: filename = os.listdir('.')
        for file in filename:
            filesize = (os.path.getsize(file))
            file_id = (generate_md5_hash(file))
            connectSocket.send(str(file_id+";"+file+";"+str(filesize)+"\n").encode())
        break
    elif request == "UPLOAD":
        connectSocket.send("Please write the file name and file size in order.".encode())
        received  = connectSocket.recv(1024).decode()
         
        filename, filesize = received.split(";")
        # remove absolute path 
        filename = os.path.basename(filename)
        # convert filesize to integer
        filesize = int(filesize)
        connectSocket.send("Ready to recieve file.".encode())
        break
        # start receiving the file from the socket
        with open(filename, "wb") as f:
            while True:
                readbytes = connectSocket.recv(1024)
                if not readbytes: 
                    break # nothing is received
                # write to the file the bytes that are just received
                f.write(readbytes)
                break
            #generate the md5 file
            server_md5 = generate_md5_hash(filename)
            f.write(server_md5)
         #send the md5 file to client
        connectSocket.send(server_md5)
        break
    elif request == "DOWNLOAD":
        connectSocket.send("Please send a file ID".encode())
        file_id  = connectSocket.recv(1024)
        file_id = file_id.decode()
        filename = os.listdir('.'),
        ids = []
        for file in filename:
            ids.append(generate_md5_hash(file))
        if file_id in ids:
            index = ids.index(file_id)
            filename = filename[index]
        if filename in os.listdir('.'):
            # start sending the file
            with open(file_id, "rb") as f:
                while True:
                    readbytes = f.read(1024)
                    if not readbytes:
                        break
                connectSocket.sendall(readbytes)
                break
#close TCP connection
connectSocket.close()
