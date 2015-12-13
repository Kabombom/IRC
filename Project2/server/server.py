import socket
import os
import sys
import json

users_and_files = {}

# TODO mudar como ver quem esta logado


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


# Function to create a socket
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


def upload(conn, filename):
    f = open(filename, 'wb')
    receive_file = conn.recv(1024)

    while receive_file:
        print('Receiving...')
        f.write(receive_file)
        receive_file = conn.recv(1024)
    print('Received')
    f.close()


def download(conn):
    filename = conn.recv(1024).decode('utf-8')
    f = open(filename, 'rb')
    receive_file = f.read(1024)
    while receive_file:
        print('Sending...')
        conn.send(receive_file)
        receive_file = f.read(1024)
    print("Finished sending")
    f.close()


def client_handler(conn, option):
    print(option)
    ################################################################
    if option == "0":
        request = conn.recv(1024)
        request = request.decode("utf-8")
        request = json.loads(request)

        write_user(request)
        conn.send("1".encode('utf-8'))

        directory = request[0] + request[1]
        if not os.path.exists(directory):
            os.makedirs(directory)

        users_and_files[directory] = []
    ################################################################
    elif option == "1":
        request = conn.recv(1024).decode("utf-8")
        request = json.loads(request)

        if read_users(request):
            conn.send("1".encode("utf-8"))
        else:
            conn.send("0".encode("utf-8"))
    ################################################################ ATE AQUI
    elif option == "2":
        request = conn.recv(1024).decode("utf-8")
        request = json.loads(request)

    ################################################################
    elif option == "3":
        request = conn.recv(1024).decode("utf-8")
        request = json.loads(request)

        filename = request[0]
        print(filename)
        user = [request[1], request[2]]
        print(user)
        path = user[0] + user[1]
        print(path)
        os.chdir(path)
        upload(conn, filename)
        os.chdir("..")
    #################################################################
    elif option == "4":
        request = ""
        user = [request[1], request[2]]
        download(conn)


def main():

    server(9000)


if __name__ == '__main__':
    main()
