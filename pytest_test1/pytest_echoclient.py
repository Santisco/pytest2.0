import socket
import sys
import time
import asyncio
import os

CLIENT_PORT = int(sys.argv[1])
CLIENT_MESSAGE = sys.argv[2]
FILE_NUM = 1
class EchoClientProtocol(asyncio.Protocol):
    SERVER_MESSAGE = CLIENT_MESSAGE
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        self.SERVER_MESSAGE = format(data.decode())

    def connection_lost(self, exc):
        # print('The server closed the connection')
        # print('Stop the event loop')
        self.loop.stop()
while True:
    loop = asyncio.get_event_loop()
    Client = EchoClientProtocol(CLIENT_MESSAGE, loop)
    coro = loop.create_connection(lambda: Client,
                                  '127.0.0.1', CLIENT_PORT)
    loop.run_until_complete(coro)
    loop.run_forever()
    if Client.SERVER_MESSAGE == '__EXIT__':
        print("SOCKET DOWN")
        loop.close()
        break
    f = open("echo_response_" + str(FILE_NUM), 'w')
    f.write("timestamp:" + str(time.time()) + "     echodata:" + CLIENT_MESSAGE)
    f.close()
    FILE_NUM = FILE_NUM + 1
    print('input message again')
    CLIENT_MESSAGE = input()
# try:
#     loop.run_forever()
# except EchoClientProtocol.data_received == '__EXIT__':
#     loop.close()
# SERVER_HOST = 'localhost'
# SERVER_PORT = int(sys.argv[1])
#
# sockets = []
# msg = str.encode(sys.argv[2])
#
# for i in range(20):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((SERVER_HOST, SERVER_PORT))
#     sockets.append(sock)
#     time.sleep(0.1)
#
# for sock in sockets:
#     sock.send(msg)
#     time.sleep(0.1)
#
# for sock in sockets:
#     data = sock.recv(1024)
#     if data != msg:
#         print('Error! No reply to', sock.getsockname())
#     time.sleep(0.1)
#
# for sock in sockets:
#     sock.close()
#     time.sleep(0.1)
