"""

register(fileobj, events, data=None)
    - fileobj나 events가 필수이고, 나머지 부가정보를 data에 넣는다.

(SelectorKey, Event)의 List <- select()
    - register 할 때 data 자리에 호출할 method 객체를 넣어놨다.
    - 그러므로 main 부분에서는 SelectorKey.data를 호출하는 형태가 된다.

"""
from collections import deque
import socket
import selectors

HOST = ''
PORT = 12000
SEL = selectors.DefaultSelector()
CONNECTIONS = {}
WAITING_USERS = deque()


# 새로운 connect이 요청됬을 때, master socket의 작업
def accept(sock):
    conn, addr = sock.accept()
    host, port = addr
    print("Connection with {}:{} was made.".format(host, port))

    if len(WAITING_USERS) == 0:
        # 연결해줄 유저가 없으므로, 큐에 추가하고 상대방이 없음을 표시
        WAITING_USERS.append(port)
        CONNECTIONS[port] = [conn, None]
    else:
        # 연결해줄 유저가 있으므로, 걔를 큐에서 빼내고 상호 파트너임을 표시
        partner = WAITING_USERS.popleft()
        CONNECTIONS[port] = [conn, partner]
        CONNECTIONS[partner][1] = port

        CONNECTIONS[port][0].send("Your partner is {}".format(partner).encode())
        CONNECTIONS[partner][0].send("Your partner is {}".format(port).encode())

    SEL.register(conn, selectors.EVENT_READ, read)


def read(conn):
    # ConnectionResetError 처리 필요
    # TODO
    data = conn.recv(1024)
    if data:
        data = data.decode()
        print("Echo to message: {}".format(data))
        conn.send("hi... {}".format(data).encode())
    else:
        print("Close connection with {}".format(conn))
        SEL.unregister(conn)
        conn.close()

# 서버 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
print("The server is ready to receive...")
server_socket.listen(10)
print("The server is ready to listen...")
SEL.register(server_socket, selectors.EVENT_READ, accept)

while True:
    events = SEL.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj)
