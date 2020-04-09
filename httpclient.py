#Anand Rao
#asr73
#CS356-008

import sys
import socket
import os.path

url=sys.argv[1]
host = url.split(":")[0]
port=url.split(':')[1].split('/')[0]
filename = url.split("/")[1]
GET=''

if not os.path.isfile("cache.txt"):
    f = open("cache.txt", "w").close()

if "Last-Modified" not in open("cache.txt").read() or filename not in open("cache.txt").read():
    GET="GET /" + filename + " HTTP/1.1" + "\\r\\n\n" + "Host: " + url.split("/")[0] + "\\r\\n\n" + "\\r\\n"
else:
    lines=open("cache.txt").read().split("\\r\\n")
    GET="GET /" + filename + " HTTP/1.1" + "\\r\\n\n" + "Host: " + url.split("/")[0] + "\\r\\n\n" + "If-Modified-Since: " + lines[2][16:] + "\\r\\n\n" + "\\r\\n"

print(GET)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, int(port)))
clientSocket.send(GET.encode())
dataEcho = clientSocket.recv(12000).decode()  

if "Not Found" in dataEcho:
    print(dataEcho)
elif "Not Modified" in dataEcho:
    print(dataEcho)
elif "Last-Modified" in dataEcho:
    f=open("cache.txt", "w")
    f.write(filename+"\n")
    f.write(dataEcho)
    f.close()
    print(dataEcho)

clientSocket.close()
