"""
Server receiver of the file
"""
import socket
import tqdm
import os


class Client:
    def __init__(self, server, port):
        self.SERVER_HOST = server
        self.SERVER_PORT = port
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPARATOR>"
        self.s = socket.socket()
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))

    def listen(self):
        self.s.listen(5)

    def accept(self):
        self.client_socket, self.address = self.s.accept()
        return (self.client_socket, self.address)

    def receive(self):
        received = self.client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        self.filename = os.path.basename(filename)
        self.filesize = int(filesize)
        return self.filename, self.filesize

    def write(self):
        with open(self.filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)

    def close(self):
        # close the client socket
        self.client_socket.close()
        # close the server socket
        self.s.close()
