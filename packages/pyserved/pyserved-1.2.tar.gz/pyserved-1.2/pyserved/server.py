"""
Client that sends the file (uploads)
"""

import socket
import tqdm
import os
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4  # 4KB

def send_file(filename, host, port):
    filesize = os.path.getsize(filename)
    s = socket.socket()
    s.connect((host, int(port)))

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            
    s.close()
