import sys
import select
from socket import *

class Server(object):
    def __init__(self, port):
        self.ep = select.epoll() # epoll类
        self.ss = socket(AF_INET, SOCK_STREAM)
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ss.bind(('', port))
        self.ss.listen(10)

        self.ep.register(self.ss.fileno(), select.EPOLLIN) # 在epoll中注册套接字（文件描述符，监听事件）

    def __del__(self):
        print('Sever is closing......')
        self.ss.close()
    
    def run(self):
        print('Server is starting......')
        # 能从套接字获得fd，从fd却不能得到套接字
        # 所以设置一个字典使得能从fd获得对应套接字
        client_dict = {} 
        while True:
            fd_event_list = self.ep.poll() # poll函数会阻塞，知道os通知其有消息到来，返回对应的fd和event
            for fd, event in fd_event_list:
                if fd == self.ss.fileno():
                    new_client, new_addr = self.ss.accept()
                    print('Welcom, the client', new_addr)
                    self.ep.register(new_client.fileno(), select.EPOLLIN)
                    client_dict[new_client.fileno()] = new_client
                elif event == select.EPOLLIN:
                    recv_data = client_dict[fd].recv(1024)
                    if recv_data:
                        client_dict[fd].send('Already have received:'.encode('utf-8'))
                        client_dict[fd].send(recv_data)
                    else:
                        print('The client has been closed.')
                        client_dict[fd].close()
                        client_dict.pop(fd)


def main():
    if len(sys.argv) == 1:
        port = 8080
    else:
        port = sys.argv[1]
    server = Server(port)
    server.run()

if __name__ == '__main__':
    main()