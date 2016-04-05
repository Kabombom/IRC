import socket
import os
import sys
import json


def read_users(user):
    file = open("users.txt", "r")
    for line in file:
        line = line.strip("\n")
        separated_info = line.split(',')
        if separated_info[0] == user[0] and separated_info[1] == user[1]:
            file.close()
            return True
    file.close()
    return False


def write_user(user):
    f = open("users.txt", "a")
    f.write(user[0] + "," + user[1] + "\n")
    f.close()


def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print("Socket creation sucefull")
    return s


def server(port):
    server_socket = create_socket(port)
    print("The server is ready to receive")
    client, address = server_socket.accept()

    while True:
        print("Connection by: ", address)
        try:
            request = client.recv(1024)
        except KeyboardInterrupt:
            sys.exit(1)
        option = request.decode("utf-8")
        client_handler(client, option)


def list_directory():
    os.listdir('')


def upload(conn, filename, size):
    f = open(filename, "wb")
    size_received = 0

    while size_received < size:
        file_bytes = conn.recv(1024)
        f.write(file_bytes)
        size_received += len(file_bytes)
    f.close()


def download(conn, request):
    f = open(request, "rb")
    read_binary = f.read(1024)
    while read_binary:
        conn.send(read_binary)
        read_binary = f.read(1024)
    f.close()


def client_handler(conn, option):
    print(option)

    if option == "0":
        request = conn.recv(1024)
        request = request.decode("utf-8")
        request = json.loads(request)

        write_user(request)
        conn.send("1".encode('utf-8'))

        directory = request[0] + request[1]
        if not os.path.exists(directory):
            os.makedirs(directory)

    elif option == "1":
        request = conn.recv(1024).decode("utf-8")
        request = json.loads(request)

        if read_users(request):
            conn.send("1".encode("utf-8"))
        else:
            conn.send("0".encode("utf-8"))

    elif option == "3":
        request = conn.recv(1024).decode("utf-8")
        request = json.loads(request)

        filename = request[0]
        size = int(request[1])
        user = [request[2], request[3]]
        path = user[0] + user[1]

        os.chdir(path)
        upload(conn, filename, size)
        os.chdir("..")

        conn.send("1".encode("utf-8"))
        print("File sucefully sent")

    elif option == "4":
        request = conn.recv(1024).decode("utf-8")
        request = json.loads(request)
        filename = request[0]
        path = request[0] + request[1]
        os.chdir(path)

        if not os.path.isfile(filename):
            conn.send("0".encode("utf-8"))
            return
        else:
            conn.send("1".encode("utf-8"))
            size = os.stat(filename).st_size
            request = str(size)
            conn.send(request.encode("utf-8"))

            f = open(request, "rb")
            read_binary = f.read(1024)
            while read_binary:
                conn.send(read_binary)
                read_binary = f.read(1024)
            f.close()


def main():
    server(9000)


if __name__ == '__main__':
    main()
