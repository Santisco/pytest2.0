
import asyncio
import time
import sys
import random
import os

FILE_NUM = 1
SERVER_PORT = sys.argv[1]

class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport
        global FILE_NUM
        f = open("web_message_" + str(FILE_NUM), 'w')
        f.write("timestamp:" + str(time.time()))
        f.close()

    def data_received(self, data):
        print('data received: {}'.format(data.decode()))
        if(data.decode() == '__EXIT__'):
            print('SERVER DOWN')
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.stop()
        global FILE_NUM
        if(os.path.exists(data.decode())):
            self.transport.write(('HTTP/1.1 200 OK   Date:' + str(time.asctime( time.localtime(time.time())) +'  '+ os.path.abspath('.'))).encode())
            f = open("web_message_" + str(FILE_NUM), 'r+')
            f.read()
            f.write("    Requested File:" + data.decode() + "    Response Code:200")
            f.close()
        else:
            self.transport.write(("HTTP/1.1 404 NOT FOUND   Date:" + str(time.asctime( time.localtime(time.time())))).encode())
            f = open("web_message_" + str(FILE_NUM), 'r+')
            f.read()
            f.write("    Requested File:" + data.decode() + "    Response Code:404")
            f.close()
        FILE_NUM = FILE_NUM + 1
        # close the socket
        self.transport.close()
        # if(data.decode == '__EXIT__'):
        #     print('NICE')
        #     global loop
        #     loop.close()

loop = asyncio.get_event_loop()
coro = loop.create_server(EchoServer, '127.0.0.1', SERVER_PORT)
server = loop.run_until_complete(coro)
print('serving on {}'.format(server.sockets[0].getsockname()) + '  PATH:' + os.path.abspath('.'))


try:
    loop.run_forever()
    loop.close()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()
