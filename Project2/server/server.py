from socket import *
import _thread


def create_user(users):
    name = input("Username: ")
    password = input("Password: ")
    new_user = [name, password]
    users.append(new_user)


def remove_user(users):
    name = input("Username to delete: ")
    pwd = input("Password to delete: ")
    for i in range(len(users)):
        if users[i][0] == name and users[i][1] == pwd:
            users.remove(i)
            return


def write_file(filename, dicio):
    file = open(filename, "w")


def read_file(filename):
    file = open(filename, "r")
    for line in file:
        print(line)


# function that takes care of CTRL+C signal
def signal_handler(signal, frame):
    print(' pressed...exiting now')


def client_handler(client, address):
    while True:
        print("Connection by: ", address)
        request = client.recv(1024)
        request = request.decode()
        if not request:
            break
        client.send("Cena")


def server(port):
    # Create an INET, streaming socket, afterwards set socket options, bind it to an adresss and start listening
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print("The server is ready to receive")

    while True:
        # Establish connection to client
        client, address = server_socket.accept()
        _thread.start_new_thread(client_handler, (client, address))


def main():
    server(9000)

if __name__ == '__main__':
    main()
