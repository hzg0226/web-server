import sys
import multiprocessing
from socket import *

class Server(object):
    def __init__(self, port, app):
        # 套接字
        self.ss = socket(AF_INET, SOCK_STREAM)
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 开启端口立即复用
        self.ss.bind(('', port))
        self.ss.listen(10)

        self.app = app
        self.env = {}
        self.header = ''

    def __del__(self):
        print('Sever is closing......')
        self.ss.close()
    
    def run(self):
        print('Server is starting......')
        while True:
            new_client, new_addr = self.ss.accept()
            print('Welcom, the client', new_addr)
            # 每来一个客户端就创建一个进程处理之
            p = multiprocessing.Process(target=self.handle_client, args=(new_client,))
            p.start()
            # 因为多进程是资源的深拷贝，所以新的子进程也会有一个client套接字，故该套接字可以关闭
            new_client.close()
    
    def handle_client(self, client):
        while True:
            recv_data = client.recv(1024)
            # 收到的数据为空时表明客户端已断开连接
            if recv_data:
                self.get_env(recv_data)
                # 由于body可能是图片、视频、文本等众多格式，故统一采用"rb"格式读取，返回的是bytes
                body = self.app(self.env, self.set_header)
                client.send(self.header.encode('utf-8'))
                client.send(body)
            else:
                print('The client has been closed.')
                client.close()
                break
    
    def get_env(self, recv_data):
        headers = recv_data.decode('utf-8').splitlines()
        headers.pop()  # header和body之间的空
        self.env['protocal'], self.env['path'], self.env['method'] = headers[0].split()
        for i in range(1, len(headers)):
            k,v = headers[i].split(':', 1)
            self.env[k] = v.strip()

    def set_header(self, status, headers):
        self.header = ''
        self.header += 'HTTP/1.1 ' + status + '\r\n'
        for temp in headers:
            self.header += '%s:%s\r\n'%temp
        # 增加与服务器有关的头
        self.header += 'Server: My server\r\n'
        self.header += '\r\n' # header和body之间的空行


def main():
    # python3 web.py 8080 mini_frame:application
    try:
        port = int(sys.argv[1])
        frame_name, app_name = sys.argv[2].split(':')

        sys.path.append('./dynamic')
        frame = __import__(frame_name)
        app = getattr(frame, app_name)
    except Exception:
        print('run as "python3 web.py 8080 mini_frame:application"')
    else:
        server = Server(port, app)
        server.run()

if __name__ == '__main__':
    main()