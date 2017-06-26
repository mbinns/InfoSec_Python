import sys
import errno
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
            print e
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
        if not sys.stdin.isatty():
            buffer = sys.stdin.read()
            if len(buffer):
                client.send(buffer)

            resp = client.recv(4096)
            print resp
            client.close()
            sys.exit()
        else:
            buffer = raw_input("")
            buffer += "\n"

        try:
            if buffer == "quit()\n":
                client.close()
                quit()

            if len(buffer):
                client.send(buffer)

            while True:
                response = ''
                recv_len = 1

                # get all of the data from the buffer
                while recv_len:
                    resp = client.recv(4096)
                    recv_len = len(resp)
                    response += resp

                    if recv_len < 4096:
                        break

                print response,

                # accept more user input
                try:
                    buffer = raw_input("")
                except EOFError:
                    sys.stdin = open('/dev/tty')
                    buffer = raw_input("")

                buffer += '\n'
                client.send(buffer)
        except Exception as e:
            print '\n' + str(e)
            client.close()
            sys.exit("FAILED Sending: {0}".format(buffer))
        except KeyboardInterrupt:
            client.close()

    def server_loop(self):
        "Setting up the listening portion of the server"
        if self.target is None:
            print 'Setting target to 0.0.0.0'
            self.target = "0.0.0.0"

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.target, self.port))

        server.listen(5)

        while True:
            client_socket, addr = server.accept()

            client_thread = threading.Thread(target=self.client_handler, args=(
                client_socket,))
            client_thread.start()

    def run_command(self, command=''):
        """Runs a command on the remote server and sends the results back
        Returns: command output"""

        # removes the newline
        command = command.rstrip()

        # run it
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                             shell=True)
        except:
            output = 'Failed to run command: {0}.\r\n'.format(command)

        return output

    def client_handler(self, client_socket):
        "Handles incoming connections to the server"
        # checks to see if the program is supposed to upload a file
        if len(self.upload_dir):
            file_buffer = ''

            # reads in data until there is none available
            while True:
                resp = client_socket.recv(1024)

                if not resp:
                    break
                else:
                    file_buffer += resp

            # write data to the remote server
            try:
                fd = open(self.upload_dir, "wb")
                fd.write(file_buffer)
                fd.close()

                # Tell the sender that the file was written
                client_socket.send("SUCCESS: File was written to: {0}\n".format(
                    self.upload_dir))
            except:
                client_socket.send("FAILURE: File was not written to: {0}\n"
                                   .format(self.upload_dir))

        # executes commands on the remote server
        if self.command:
            while True:
                # show a prompt
                try:
                    # recieve until enter is pressed
                    cmd_buffer = client_socket.recv(1024)
                    if cmd_buffer:
                        resp = self.run_command(cmd_buffer)
                        client_socket.send(resp + "MACK:#>")
                    else:
                        client_socket.send("MACK:#> ")

                except KeyboardInterrupt:
                    client_socket.send("Server shutting down...")
                    sys.exit(0)
                except socket.error as e:
                    if e.errno == errno.EPIPE:
                        print 'Client Disconnected'
                        break


def main():
    nc = net_tool()
    if len(sys.argv) > 1:
        nc.setup()
        print "Setting up using command line args"
    else:
        nc.target = str(raw_input("Enter target: "))
        nc.port = int(raw_input("Enter port: "))

    if nc.listen:
        nc.server_loop()
    else:
        print 'sending commands'
        print 'MACK:#>',
        nc.sender()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Shutting Down...'
        sys.exit(0)
