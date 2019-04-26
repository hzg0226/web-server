import time

# 路由字典，path-func
URL_FUNC = dict()

# 路由装饰器
def route(url):
    def set_func(func):
        URL_FUNC[url] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func

@route('/index.html')
def index():
    with open('./templates/index.html', 'rb') as f:
        content = f.read()
    return content

@route('/center.html')
def center():
    with open('./templates/center.html', 'rb') as f:
        content = f.read()
    return content

@route('/login.html')
def login():
    return '<h1>login</h1>'.encode('utf-8')

@route('/register.html')
def register():
    return '<h1>register</h1>'.encode('utf-8')


def application(env, start_response):
    path = env['path']
    flag = True
    if path == '/':
        path = '/index.html' # default page is the index.html
    
    try:
        if path in URL_FUNC.keys():
            # dynamic file
            body = URL_FUNC[path]()
        else:
            # static file
            f = open('./static'+path, 'rb')
            body = f.read()
    except Exception:
        body = '<h1>404, not found</h1>'.encode('utf-8')
        status = '404 NOT FOUND'
    else:
        status = '200 OK'

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