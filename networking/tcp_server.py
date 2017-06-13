import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

# create the socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the server to the ip and port of the computer specified
server.bind((bind_ip, bind_port))

# tell the server to sit and listen, the 5 is total number of connections
# supported
server.listen(5)
print 'Server listening on'
print '======================='
print 'IP: {0}'.format(bind_ip)
print 'Port: {0}'.format(bind_port)


def handle_client(client_socket):
    # print what the client says

    while True:
        data = client_socket.recv(1024)
        if not data:
            client_socket.close()
            break
        else:
            # reply to the client
            client_socket.send("ACK : {0}".format(data))
            print data,


# main server loop
while True:
    # get the client object and the information about the client
    client, addr = server.accept()

    print '======================='
    print 'Accepted connection from'
    print '======================='
    print 'IP: {0}'.format(addr[0])
    print 'Port: {0}'.format(addr[1])

    # give the client a thread
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
