#Anand Rao
#asr73
#CS356-008

import sys
import socket
import datetime
import time
import os.path

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
dataLen = 1000000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)


while True:
    connectionSocket, address = serverSocket.accept()
    data = connectionSocket.recv(dataLen).decode()
    filename=data.split('/')[1].split(' ')[0]
    t = datetime.datetime.utcnow()
    currentdate = t.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response=''    

    if not os.path.isfile(filename):
        response= "HTTP/1.1 404 Not Found" + "\\r\\n\n" + "Date: " + currentdate + "\\r\\n\n" + "\\r\\n" 
    else:
        lastmodfile=time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime(filename)))
        lastmodcache=time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime("cache.txt")))
        if "If-Modified-Since" not in data or lastmodfile>lastmodcache:
            f=open(filename, 'r')
            content=f.read()
            f.close()
            response= "HTTP/1.1 200 OK" + "\\r\\n\n" + "Date: " + currentdate  + "\\r\\n\n" + "Last-Modified: " + lastmodfile + "\\r\\n\n" + "Content-Length: " + str(len(content)) + "\\r\\n\n" + "Content-Type: text/html; charset=UTF-8" + "\\r\\n\n" + "\\r\\n\n" + content
        elif lastmodfile<lastmodcache:
            response= "HTTP/1.1 304 Not Modified"+ "\\r\\n\n" + "Date: " + currentdate + "\\r\\n\n" + "\\r\\n"


    connectionSocket.send(response.encode())
