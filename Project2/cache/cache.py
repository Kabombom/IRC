import socket
import os
import sys
import json

def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print("Socket creation sucefull")
    return s


def cache(port):
    server_socket = create_socket(port)
    print("The server is ready to receive")

    while True:
        client, address = server_socket.accept()
        print("Connection by: ", address)

        try:
            request = client.recv(1024)
            request = request.decode("utf-8")
            request = json.loads(request)
        except socket.error as e:
            print("Error receiving data %s". e)

