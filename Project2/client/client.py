import socket
import sys
import json
import os


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


def create_socket(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print('Unable to connect, exception type %s' % e)
        sys.exit()
    print("Socket creation sucefull")


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
