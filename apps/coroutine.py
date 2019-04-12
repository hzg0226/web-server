import gevent
from gevent import monkey
monkey.patch_all()
# 打补丁需要在import的库之前，否则打补丁会失败
# 所以一般打补丁放在最前面
import sys
from socket import *

class Server(object):
    def __init__(self, port):
        self.ss = socket(AF_INET, SOCK_STREAM)
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ss.bind(('', port))
        self.ss.listen(10)

    def __del__(self):
        print('Sever is closing......')
        self.ss.close()
    
    def run(self):
        print('Server is starting......')
        while True:
            new_client, new_addr = self.ss.accept()
            print('Welcom, the client', new_addr)
            gevent.spawn(self.handle_client, new_client)
            # 这里没有使用g.join()，这是因为socket中的recv，accpet等诸多函数都会阻塞
            # 不需要人为阻塞使协程工作

    def handle_client(self, client):
        while True:
            recv_data = client.recv(1024)
            if recv_data:
                client.send('Already have received:'.encode('utf-8'))
                client.send(recv_data)
            else:
                print('The client has been closed.')
                client.close()
                break

def main():
    if len(sys.argv) == 1:
        port = 8080
    else:
        port = sys.argv[1]
    server = Server(port)
    server.run()

if __name__ == '__main__':
    main()