import sys
import os
import socket
import parser
from threading import Thread

class Proxy2Server(Thread):
    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        # client is defined in Local2Proxy and will be exchanged with this
        # object
        self.host = host
        self.port = port
        self.client = None

        # create socket for server connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        while True:

            # grab 4 bytes of data from server
            data = self.server.recv(4096)
            if data:
                try:
                    # check for changes in the parser
                    reload(parser)

                    # basic hex dump function
                    parser.hexdump(data, 'client')
                except Exception as e:
                    print e

                # send all data to the server
                self.client.sendall(data)


class Local2Proxy(Thread):
    def __init__(self, host, port):
        super(Local2Proxy, self).__init__()

        # client connection information
        self.host = host
        self.port = port

        # server is unknown currently
        # will get server from the Proxy2Server class
        self.server = None

        # create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # reuse socket that is currently waiting for time_out
        # stops the 'failed to bind' error from running to back to back
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds to the address and port specified by the run time args
        # for local hosts
        sock.bind((host, port))

        #only accept 1 connection
        sock.listen(1)

        # wait for conenction
        # creates the client object
        # self.client = returned socket, addr is the address of the client
        self.client, addr = sock.accept()

    def run(self):
        while True:

            # get data from the client
            data = self.client.recv(4096)
            if data:
                try:
                    # check for changes in parser
                    reload(parser)

                    # basic hex dump function
                    parser.hexdump(data, 'server')
                except Exception as e:
                    print e
                self.server.sendall(data)


class Proxy(Thread):
    def __init__(self, local, remote):
        super(Proxy, self).__init__()
        self.local_host, self.local_port = local
        self.remote_host, self.remote_port = remote

    def run(self):
        while True:
            # create the threads for client and remote sockets
            self.l2p = Local2Proxy(self.local_host, self.local_port)
            self.p2s = Proxy2Server(self.remote_host, self.remote_port)

            print "proxy({}) established".format(self.local_port)

            # exchange sockets
            # this defined the clients and servers for each socket
            # client is made in the l2p and given to the p2s
            # the server is made in p2s and given to l2p
            # pass by reference
            self.l2p.server = self.p2s.server
            self.p2s.client = self.l2p.client

            #start server
            self.l2p.start()
            self.p2s.start()


def main():
    # local host to listen on
    if len(sys.argv[1:]) != 4:
        print "Usage: ./proxy <local_host> <local_port> <remote_host> <remote_port>"
        print "Ex: ./proxy 127.0.0.1 80 google.com 80"
        os._exit(1)

    # local binding information
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # remote server
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # Start proxy
    master_server = Proxy((local_host, local_port), (remote_host, remote_port))
    master_server.start()

    # capture 'quit' and ctrl-c to exit program
    while True:
        try:
            cmd = raw_input('$ ')
            if cmd[:4] == 'quit':
                os._exit(0)
        except Exception as e:
            print e
        except KeyboardInterrupt:
            os._exit(0)

main()
