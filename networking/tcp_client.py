import socket


host = "0.0.0.0"
port = 9999

# create the socket object
# SOCK_STREAM denotes TCP connections
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
client.connect((host, port))

# send stuff
stuff = raw_input("SEND: ")
client.send(stuff)

# anything more than 4096 will be truncated
print client.recv(4096)
