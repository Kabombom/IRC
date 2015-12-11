import socket
import os
import json


def read_users():
    file = open("users.txt", "r")
    lines = []
    for line in file:
        lines.append(line)
    return lines


def write_user(user):
    with open("users.txt", "a") as myfile:
        myfile.write(user)


def read_file(filename):
    lines = []
    with open(filename, "r") as file:
        for line in file:
            lines.append(line)
    return lines


def write_file(filename, lines):
    with open(filename, "w") as file:
        for i in range(len(lines)):
            file.write(lines[i])


def confirm_login(login_credentials):
    users = read_users()
    for user in users:
        if login_credentials[0] == user[0] and login_credentials[1] == user[1]:
            return True
    return False


def register():
    name = input("Username: ")
    password = input("Password: ")
    new_user = [name, password]
    write_user(new_user)


def remove_user():
    users = read_users()
    name = input("Username to delete: ")
    pwd = input("Password to delete: ")
    for i in range(len(users)):
        if users[i][0] == name and users[i][1] == pwd:
            users.remove(i)


def login():
    name = input("Username: ")
    pwd = input("Password: ")
    user = [name, pwd]
    while not confirm_login(user):
        print("Invalid input")
        name = input("Username: ")
        pwd = input("Password: ")
        user = [name, pwd]
    return [name, pwd]


def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print("Socket creation sucefull")
    return s


def server(port):
    # Create an INET, streaming socket, afterwards set socket options, bind it to an adresss and start listening
    server_socket = create_socket(port)
    print("The server is ready to receive")

    while True:
        # Establish connection to client
        client, address = server_socket.accept()
        print("Connection by: ", address)
        request = client.recv(1024)
        request = request.decode("utf-8")
        request = json.loads(request)

        client_handler(client, request)


def list_directory():
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


def main():
    server(9000)


if __name__ == '__main__':
    main()
