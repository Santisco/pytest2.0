
import asyncio
import time
import sys

FILE_NUM = 1
SERVER_PORT = sys.argv[1]
class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport
        global FILE_NUM
        f = open("echo_message_" + str(FILE_NUM), 'w')
        f.write("timestamp:" + str(time.time()) + "    IP&PORT:"+format(peername))
        f.close()

    def data_received(self, data):
        print('data received: {}'.format(data.decode()))
        self.transport.write(data)
        if(data.decode() == '__EXIT__'):
            print('SERVER DOWN')
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.stop()
        global FILE_NUM
        f = open("echo_message_" + str(FILE_NUM), 'r+')
        f.read()
        f.write("    echo_message :"+data.decode())
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
print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
    loop.close()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()
