import socket

host = "localhost"
port = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("Connection was made...")
response = client_socket.recv(2048)
print(response.decode())

while True:
    name = input("write your name: ")
    # client_socket.sendall(name.encode())
    response = client_socket.recv(2048)
    print(response.decode())
