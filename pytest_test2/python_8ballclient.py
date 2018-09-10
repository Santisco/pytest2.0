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
        f = open("8ball_response_" + str(FILE_NUM), 'r+')
        f.read()
        f.write("    answer:" + data.decode())
        f.close()

    def connection_lost(self, exc):
        # print('The server closed the connection')
        # print('Stop the event loop')
        self.loop.stop()
while True:
    f = open("8ball_response_" + str(FILE_NUM), 'w')
    f.write("timestamp:" + str(time.time()) + "     question:" + CLIENT_MESSAGE)
    f.close()
    loop = asyncio.get_event_loop()
    Client = EchoClientProtocol(CLIENT_MESSAGE, loop)
    coro = loop.create_connection(lambda: Client,
                                  '127.0.0.1', CLIENT_PORT)
    loop.run_until_complete(coro)
    if CLIENT_MESSAGE == '__EXIT__':
        print("SOCKET DOWN")
        loop.close()
        break
    loop.run_forever()
    FILE_NUM = FILE_NUM + 1
    print('input message again')
    CLIENT_MESSAGE = input()
