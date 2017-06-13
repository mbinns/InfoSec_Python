import socket


host = "www.google.com"
port = 80

# create the socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
client.connect((host, port))

# send stuff
# this doesn't have to be http
client.send("GET / HTTP/1.1\r\n\Host: google.com\r\n\r\n")

print client.recv(4096)
