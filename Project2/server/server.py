import socket
import os
import json


def confirm_login(filename, login_credentials):
    users = read_file(filename)
    for user in users:
        if login_credentials[0] == user[0] and login_credentials[1] == user[1]:
            return True
    return False


def login(filename):
    name = input("Username: ")
    pwd = input("Password: ")
    user = [name, pwd]
    while not confirm_login(filename, user):
        print("Invalid input")
        name = input("Username: ")
        pwd = input("Password: ")
        user = [name, pwd]
    return [name, pwd]


def register(filename):
    name = input("Username: ")
    password = input("Password: ")
    new_user = [name, password]
    file_lines = read_file(filename)
    file_lines.append(new_user)
    write_file(filename, file_lines)


def remove_user(users):
    name = input("Username to delete: ")
    pwd = input("Password to delete: ")
    for i in range(len(users)):
        if users[i][0] == name and users[i][1] == pwd:
            users.remove(i)


def write_file(filename):
    file = open(filename, "w")
    file_lines = read_file(filename)
    for line in file_lines:
        file.write(line)


def read_file(filename):
    file = open(filename, "r")
    file_lines = []
    for line in file:
        file_list = line.split(',')
        file_lines.append(file_list)
    return file_lines


def list():
    os.listdir('')


def upload(filename, file_lines):
    file = open(filename, "w")
    for line in file_lines:
        file.write(line)


def client_handler(client, request):
    if isinstance(request, int):
        if int(request) == 0:
            register("users.txt")
        elif int(request) == 1:
            login("users.txt")
        elif int(request) == 2:
            list()
        elif int(request) == 4:
            filename = input("Filename: ")
            data = read_file(filename)
            data_string = json.dumps(data).encode('utf-8')
            client.send(data_string)
        elif int(request) == 5:
            return

    if isinstance(request, tuple):
        filename = str(request[0])
        lines = request[1]
        upload(filename, lines)


def server(port):
    # Create an INET, streaming socket, afterwards set socket options, bind it to an adresss and start listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print("The server is ready to receive")

    while True:
        # Establish connection to client
        client, address = server_socket.accept()
        print("Connection by: ", address)
        request = client.recv(1024)
        request = request.decode("utf-8")
        request = json.loads(request)

        client_handler(client, request)


def main():
    server(9000)


if __name__ == '__main__':
    main()
