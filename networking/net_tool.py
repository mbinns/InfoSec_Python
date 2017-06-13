import sys
import socket
import getopt
import threading
import subprocess


class net_tool(object):
    def __init__(self, l=False, c=False, u=False, e=False, d=''):
        # tool settings
        self.listen = l
        self.command = c
        self.upload = u
        self.execute = e
        self.target = None
        self.upload_dir = d
        self.port = 0

    def setup(self):
        "Initializes tool settings from command line arguments"
        # get the arguments from the command line
        # target and port are mandatory arguments
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                       ["help", "listen", "target", "port",
                                        "command", "upload"])
        except getopt.GetoptError as e:
            print str(e)

        # checks and sets arguments
        for o, a in opts:
            if o in ('-h', '--help'):
                print "help me!"
            elif o in ('-l', '--listen'):
                self.listen = True
            elif o in ('-e', '--execute'):
                self.execute = True
            elif o in ('-c', '--commandshell'):
                self.command = True
            elif o in ('-u', '--upload'):
                self.upload_dir = a
            elif o in ('-t', '--target'):
                self.target = str(a)
            elif o in ('-p', '--port'):
                self.port = int(a)
            else:
                sys.exit('Unknown parameter, quitting')

    def listener(self):
        "Starts the tool in listening mode"

    def sender(self, buffer=''):
        "Sends data to the target and port"
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            if self.target is not None and self.port is not 0:
                client.connect((self.target, self.port))
            else:
                print "target:{0} or port:{1} malformed".format(
                    self.target, self.port)
        except:
            print "target:{0} or port:{1} malformed".format(
                self.target, self.port)
            sys.exit("Connection to target Failed, check IP and Port")

        # check for stdin input
        if buffer == '':
            buffer = sys.stdin.read()

        try:
            if len(buffer):
                client.send(buffer)

            while True:
                response = ''

                # get all of the data from the buffer
                while True:
                    resp = client.recv(4096)
                    response += resp

                    if len(resp) < 4096:
                        break

                print response,

                # accept more user input
                buffer = raw_input("Send: ")
                buffer += "\n"

                client.send(buffer)
        except:
            client.close()
            sys.exit("FAILED Sending: {0}".format(buffer))

    def run_command(self, command):
        "Runs a command on the remote computer"


nc = net_tool()
if len(sys.argv) > 1:
    nc.setup()
    print "Setting up using command line args"
else:
    nc.target = str(raw_input("Enter target: "))
    nc.port = int(raw_input("Enter port: "))

nc.sender()
