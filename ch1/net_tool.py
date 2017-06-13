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
                self.target = a
            elif o in ('-p', '--port'):
                self.port = int(a)
            else:
                sys.exit('Unknown parameter, quitting')

    def listener(self):
        "Starts the tool in listening mode"

    def sender(self):
        "Sends data to the target and port"

    def run_command(self, command):
        "Runs a command on the remote computer"
