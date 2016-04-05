import socket
import sys
import json
import os


def create_socket(port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(e)
        sys.exit(1)
    try:
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        print(e)
        sys.exit(1)

    host = socket.gethostname()
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(e)
        sys.exit(1)
    print("Socket creation sucefull")
    return client_socket


def check_if_file_exists(filename):
    try:
        f = open(filename)
    except IOError:
        print("File doesn't exist")
        return False
    f.close()
    return True


def login_or_register(choice):
    if choice == 0:
        name = str(input("Username to register: "))
        pwd = str(input("Password to register: "))
        user = [name, pwd]
        request = json.dumps(user)
    else:
        name = str(input("Username: "))
        pwd = str(input("Password: "))
        user = [name, pwd]
        request = json.dumps(user)
    return request


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
    return str(option)


def main():
    users_and_files = {}
    loggedin_user = []
    server_port = 9000
    conn = create_socket(server_port)
    cache_conn = create_socket(9002)

    while True:
        choice = menu()
        if choice == "0":
            conn.send(choice.encode("utf-8"))

            request = login_or_register(0)
            conn.send(request.encode("utf-8"))

            server_response = conn.recv(1024).decode("utf-8")
            if server_response == "1":
                print("Client registration successfull")

        elif choice == "1":
            conn.send(choice.encode("utf-8"))

            request = login_or_register(1)
            conn.send(request.encode("utf-8"))

            server_response = conn.recv(1024).decode("utf-8")

            if server_response == "1":
                loggedin_user = json.loads(request)
                print(loggedin_user)
                print("Logged to the server!")
            else:
                print("Error tryig to login")

        elif choice == "2":
            for key in users_and_files:
                print(users_and_files[key])

        elif choice == "3":
            conn.send(choice.encode('utf-8'))

            filename = str(input("Filename to upload: "))
            while not check_if_file_exists(filename):
                filename = str(input("Filename to upload: "))

            size = os.stat(filename).st_size
            size = str(size)
            request = [filename, size, loggedin_user[0], loggedin_user[1]]
            request = json.dumps(request)
            conn.send(request.encode("utf-8"))
            f = open(filename, "rb")
            read_binary = f.read(1024)
            while read_binary:
                conn.send(read_binary)
                read_binary = f.read(1024)
            f.close()

            response = conn.recv(1024).decode("utf-8")
            if response == "1":
                print("File sucefully sent")
                key = loggedin_user[0] + loggedin_user[1]
                if key in users_and_files:
                    users_and_files[key].append(filename)
                else:
                    users_and_files[key] = [filename]

            else:
                print("Error sending file")

        elif choice == "4":
            filename = str(input("Filename to download: "))
            cache_request = [filename, loggedin_user[0], loggedin_user[1]]
            cache_request = json.dumps(cache_request)
            cache_conn.send(cache_request.encode("utf-8"))

        elif choice == 5:
            return


if __name__ == '__main__':
    main()
