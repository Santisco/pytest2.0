
import asyncio
import time
import sys

def toAlpha(c,i):
    c = c.lower()
    num = ord(c)
    if num >= 97 and num <= 122:
        num = 97 + ((num - 97) + i) % 26
    return chr(num)

#string 明文  i 移位参数
def encrypt(string,i):
    string_new = ''
    for s in string:
        string_new += str(toAlpha(s,i))
    return string_new

#string 密文  i 移位参数
def decrypt(string,i):
    return encrypt(string,-i)

FILE_NUM = 1
SERVER_PORT = sys.argv[1]
class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport
        global FILE_NUM
        f = open("security_message_" + str(FILE_NUM), 'w')
        f.write("timestamp:" + str(time.time()))
        f.close()

    def data_received(self, data):
        print('data received: {}'.format(data.decode()))
        datastring = data.decode()
        secure = datastring
        if(datastring[0:8] == 'decrypt,'):
            self.transport.write((str(decrypt(datastring[8:], 3)) + ',P').encode())
            secure = str(decrypt(datastring[8:], 3))
        elif(datastring[0:8] == 'encrypt,'):
            self.transport.write((str(encrypt(datastring[8:], 3)) + ',C').encode())
            secure = str(encrypt(datastring[8:], 3))
        if(data.decode() == '__EXIT__'):
            print('SERVER DOWN')
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.stop()
        global FILE_NUM
        f = open("security_message_" + str(FILE_NUM), 'r+')
        f.read()
        f.write("    security_message :"+data.decode()+"    security_response:"+secure)
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
