import sys
import multiprocessing
from socket import *

def handle_client(client):
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
    
    ss = socket(AF_INET, SOCK_STREAM)
    ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 开启端口立即复用
    ss.bind(('', port))
    ss.listen(10)
    po = multiprocessing.Pool(10) # 进程池大小为10

    while True:
        new_client, new_addr = ss.accept()
        print('Welcom, the client', new_addr)
        # 每来一个客户端就将其扔进进程池
        po.apply_async(handle_client, (new_client, ))

    po.close()
    po.join()

if __name__ == '__main__':
    main()

'''以下用类实现的进程池不能实现多任务
import sys
import multiprocessing
from socket import *

class Server(object):
    def __init__(self, port):
        self.ss = socket(AF_INET, SOCK_STREAM)
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 开启端口立即复用
        self.ss.bind(('', port))
        self.ss.listen(10)
        self.po = multiprocessing.Pool(10) # 进程池大小为10

    def __del__(self):
        print('Sever is closing......')
        self.ss.close()
    
    def run(self):
        print('Server is starting......')
        while True:
            new_client, new_addr = self.ss.accept()
            print('Welcom, the client', new_addr)
            # 每来一个客户端就创建一个进程处理之
            self.po.apply_async(self.handle_client, (new_client,))
        self.po.close()
        self.po.join()
    
    def handle_client(self, client):
        while True:
            recv_data = client.recv(1024)
            # 收到的数据为空时表明客户端已断开连接
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
'''