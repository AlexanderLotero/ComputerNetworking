#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    serverSocket.bind(("", port))
    #Fill in start
    serverSocket.listen(1)                                       # found in Python "socket" documentation, with help from socket tutorial, one request at a time
    #Fill in end

    while True:
        #Establish the connection
        # print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()          # found in Python "socket" documentation
        # print(addr)
        # print("connection established")
        try:
            message = connectionSocket.recv(4096)               # found in Python "socket" documentation, "the value of bufsize should be a relatively small power of 2, for example, 4096"
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()                               # stack overflow: read a text file into a string variable

            #Send one HTTP header line into socket
            #Fill in start
            httpOK = "HTTP/1.1 200 OK\r\n"                       # taken from Wireshark lab (http4.pcapng), GET response output
            connectionSocket.send(httpOK.encode('utf-8'))        # to alleviate TypeError: a bytes-like object is required, not 'str'
            #Fill in end

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            #Send response message for file not found (404)
            #Fill in start
            httpNotFound = "HTTP/1.1 404 Not Found\r\n"         # taken from Wireshark lab (http4.pcapng), GET response output
            connectionSocket.send(httpNotFound.encode('utf-8')) # to alleviate TypeError: a bytes-like object is required, not 'str'
            #Fill in end

            #Close client socket
            #Fill in start
            connectionSocket.close()                            # found in Python "socket" documentation
            #Fill in end

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)