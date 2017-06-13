import socket


host = "127.0.0.1"
port = 80

# create a that handles UDP connections
# SOCK_DGRAM denotes UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto("TESTSTRING", (host, port))

# recive some data
# comes back in a tuple with the data and the address it came from
data, addr = client.recvfrom(4096)
print data
