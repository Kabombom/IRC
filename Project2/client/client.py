import socket
import sys
import json
import os


def read_file(filename):
    file = open(filename, "r")
    file_lines = []
    for line in file:
        file_list = line.split(',')
        file_lines.append(file_list)
    return file_lines


def write_file(filename, lines):
    file = open(filename, "w")
    file_lines = read_file(filename)
    for list in file_lines:
        file.write(list)


def upload(filename):
    lines = read_file(filename)
    return lines


def filename_validation(filename):
    if not os.path.isfile(filename):
        return False
    return True


def filename_input():
    filename = input("Filename: ")
    while not filename_validation(filename):
        filename = input("Invalid input, filename: ")
    return filename


def options_validation(option):
    try:
        choice = int(option)
        if choice < 0 or choice > 5:
            return False
        return True
    except ValueError:
        print("Invalid input")
        return False


def menu():
    option = input("[0]--> Register\n"
                   "[1]--> Login\n"
                   "[2]--> List\n"
                   "[3]--> Upload\n"
                   "[4]--> Download\n"
                   "[5]--> Exit\n"
                   "What do you wish to do: ")
    while not options_validation(option):
        option = input("Invalid input\n"
                       "[0]--> Register\n"
                       "[1]--> Login\n"
                       "[2]--> List\n"
                       "[3]--> Upload\n"
                       "[4]--> Download\n"
                       "[5]--> Exit\n"
                       "What do you wish to do: ")
    return int(option)


def client(port, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket creation sucefull")
    host = socket.gethostname()
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print('Unable to connect, exception type %s' % e)
        sys.exit()

    if isinstance(data, int):
        data_string = str(data)
        client_socket.send(data_string.encode('utf-8'))
    if isinstance(data, list) or isinstance(data, dict):
        data_string = json.dumps(data).encode('utf-8')
        client_socket.send(data_string)


def main(client_socket):
    port = 9000
    while True:
        choice = menu()
        if choice == 0:
            client(port, 0)
        elif choice == 1:
            client(port, 1)
        elif choice == 2:
            client(port, 2)
        elif choice == 3:
            filename = filename_input()
            lines = upload(filename)
            to_send = (filename, lines)
            client(port, to_send)
        elif choice == 4:
            client(port, 4)
            request = client_socket.recv(1024)
            request = request.decode('utf-8')
            request = json.loads(request)
            write_file()
        elif choice == 5:
            return


if __name__ == '__main__':
    main()
