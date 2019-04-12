import sys
from socket import *

class Server(object):
    def __init__(self, port):
        self.ss = socket(AF_INET, SOCK_STREAM)
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ss.setblocking(False) # 非阻塞模式
        self.ss.bind(('', port))
        self.ss.listen(10)

    def __del__(self):
        print('Sever is closing......')
        self.ss.close()
    
    def run(self):
        print('Server is starting......')
        client_list = [] # 已连接客户端列表，轮询
        while True:
            # 判断是否有新的客户端到来
            try:
                new_client, new_addr = self.ss.accept()
            except Exception:
                pass
            else:
                print('Welcom, the client', new_addr)
                client_list.append(new_client)
                new_client.setblocking(False)
            # 判断是否有新的消息到来
            for client in client_list:
                try:
                    recv_data = client.recv(1024)
                except Exception:
                    pass
                else:
                    if recv_data:
                        client.send('Already have received:'.encode('utf-8'))
                        client.send(recv_data)
                    else:
                        print('The client has been closed.')
                        client.close()
                        client_list.remove(client)
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