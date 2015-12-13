import socket
import sys
import json
import signal

# TODO proteçao se nao estiver logado


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
    users = {}
    loggedin_user = []
    server_port = 9000
    conn = create_socket(server_port)

    while True:
        choice = menu()
        ###################################################################
        if choice == "0":
            conn.send(choice.encode("utf-8"))

            request = login_or_register(0)
            conn.send(request.encode("utf-8"))

            server_response = conn.recv(1024).decode("utf-8")
            print(server_response)
            if server_response == "1":
                print("Client registration successfull")
        #####################################################################
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
        ######################################################################### ATE AQUI
        elif choice == "2":
            conn.send(choice.encode("utf-8"))

            request = json.dumps(loggedin_user)
            conn.send(request.encode("utf-8"))


        ######################################################################### COMEÇA aqui
        elif choice == "3":
            conn.send(choice.encode('utf-8'))

            filename = str(input("Filename to upload: "))
            while not check_if_file_exists(filename):
                filename = str(input("Filename to upload: "))

            request = [filename, loggedin_user[0], loggedin_user[1]]
            request = json.dumps(request)
            conn.send(request.encode("utf-8"))

            f = open(filename, "rb")
            read_binary = f.read(1024)
            while read_binary:
                print("Sending...")
                conn.send(read_binary)
                read_binary = f.read(1024)
                if
            print("Finished sending")
            f.close()
        ##############################################################################
        elif choice == "4":
            conn.send(str(choice).encode("utf-8"))

            filename = str(input("Filename to download: "))
            conn.send(filename.encode('utf-8'))

            f = open(filename, 'wb')
            server_response = conn.recv(1024)
            while server_response:
                print("Receiving...")
                f.write(server_response)
                server_response = conn.recv(1024)
            print('Received')
            f.close()
        ################################################################################
        elif choice == 5:
            return


def signal_handler(signal, frame):
    print(' pressed...exiting now')
    sys.exit(0)


if __name__ == '__main__':
    main()
