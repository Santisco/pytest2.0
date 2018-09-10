
import asyncio
import time
import sys
import random

FILE_NUM = 1
SERVER_PORT = sys.argv[1]
list = ['Your guess is as good as mine.', 'You need a vacation.', 'It\'s Trump\'s fault!', 'I don\'t know. What do you think?',
        'Nobody ever said it would be easy, they only said it would be worth it.', 'You really expect me to answer that?',
        'You\'re going to get what you deserve.', 'That depends on how much you\'re willing to pay.']
dict = {'':''}
class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport
        global FILE_NUM
        f = open("8ball_message_" + str(FILE_NUM), 'w')
        f.write("timestamp:" + str(time.time()))
        f.close()

    def data_received(self, data):
        print('data received: {}'.format(data.decode()))
        if(data.decode() == '__EXIT__'):
            print('SERVER DOWN')
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.stop()
            self.transport.write('__EXIT__'.encode())
            self.transport.close()
        global dict
        answer = ''
        if data.decode() in dict:
            self.transport.write(dict[data.decode()].encode())
            answer = dict[data.decode()]
        else:
            num = random.randint(0, 7)
            dict[data.decode()] = list[num]
            self.transport.write(list[num].encode())
            answer = list[num]
        global FILE_NUM
        f = open("8ball_message_" + str(FILE_NUM), 'r+')
        f.read()
        f.write("    question :"+data.decode() + "    answer:" + answer)
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
