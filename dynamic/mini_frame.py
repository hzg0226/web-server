import time

def index():
    with open('./templates/index.html', 'rb') as f:
        content = f.read()
    return content

def center():
    with open('./templates/center.html', 'rb') as f:
        content = f.read()
    return content
    
def login():
    return '<h1>login</h1>'.encode('utf-8')

def register():
    return '<h1>register</h1>'.encode('utf-8')

def application(env, start_response):
    path = env['path']
    flag = True
    if path == '/':
        path = '/index.py' # default page is the index.html
    
    if not path.endswith('.py'):
        # static file
        try:
            f = open('./static'+path, 'rb')
            body = f.read()
        except Exception as ret:
            flag = False
            body = b''
            print(ret)
    else:
        # dynamic file
        if path == '/index.py':
            body = index()
        elif path == '/center.py':
            body = center()
        else:
            flag = False
            body = '<h1>404, not found</h1>'.encode('utf-8')
    
    if flag:
        status = '200 OK'
    else:
        status = '404 NOT FOUND'

    headers = [
        ('Connection', 'Keep-Alive'),
        # ('Content-Type', 'text/html'),
        ('Content-Length', '%d'%len(body))
    ]
    # Connection：Keep-Alive保持长连接，close关闭长连接。
    # Content-Type：text/html;charset=utf-8，网页显示中文，但是其他编码出问题，所以不通用。
    # Content-Length：body的长度。要实现长连接需要加上此，否则浏览器会一直转圈。

    start_response(status, headers)
    # 返回的body必须是bytes类型
    return body