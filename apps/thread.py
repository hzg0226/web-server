import sys
import threading
from socket import *

class Server(object):
    def __init__(self, port):
        self.ss = socket(AF_INET, SOCK_STREAM)
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 开启端口立即复用
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
            # 每来一个客户端就创建一个线程处理之
            t = threading.Thread(target=self.handle_client, args=(new_client,))
            t.start()
    
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