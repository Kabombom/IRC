import socket
import os
import json


def server_com_socket(port):
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    server_conn.connect((host, port))
    print("Socket creation sucefull")
    return server_conn


def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print("Socket creation sucefull")
    return s


def cache(port):
    cache_socket = create_socket(port)
    print("The cache is ready to receive")
    client, address = cache_socket.accept()
    server_conn = server_com_socket(9000)
    while True:
        print("Connection by: ", address)
        request = client.recv(1024)
        request = request.decode("utf-8")
        download_handler(server_conn, client, request)


def download_handler(server_conn, conn, request):
    data = json.loads(request)
    filename = data[0]
    print(filename)
    if not os.path.isfile(filename):
        server_conn.send("4".encode("utf-8"))
        server_conn.send(request.encode("utf-8"))

        server_response = server_conn.recv(1024)
        server_response = server_response.decode("utf-8")
        print(server_response)
        if server_response == "1":
            f = open(filename, "wb")
            size = int(server_conn.recv(1024).decode("utf-8"))
            print(size)
            size_received = 0
            while size_received < int(size):
                file_bytes = conn.recv(1024)
                f.write(file_bytes)
                size_received += len(file_bytes)
            f.close()

        else:
            conn.send("0".encode("utf-8"))
            print("test222")
            return

    else:
        conn.send("1".encode("utf-8"))
        size = os.stat(filename).st_size
        size = str(size)
        request = [filename, size]
        print(size)
        request = json.dumps(request).encode("utf-8")
        conn.send(request)

        f = open(filename, "rb")
        read_binary = f.read(1024)
        while read_binary:
            conn.send(read_binary)
            read_binary = f.read(1024)
        f.close()


if __name__ == '__main__':
    cache(9002)
