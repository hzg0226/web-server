def login():
    return '<h1>login</h1>'

def register():
    return '<h1>register</h1>'

def app(path):
    flag = True
    if path == '/login.py':
        body = login()
    elif path == 'register.py':
        body = register()
    else:
        flag = False
        body = '<h1>404, not found</h1>'
    
    haha = [
        'Connection: Keep-Alive',
        'Content-Length: %d' % len(body)
    ]
    if flag:
        header = 'HTTP/1.1 200 OK\r\n' + '\r\n'.join(haha) + '\r\n\r\n'
    else:
        header = 'HTTP/1.1 404 NOT FOUND\r\n' + '\r\n'.join(haha) + '\r\n\r\n'
    
    return header, body

def application(env, start_response):
    path = env['path']
    flag = True
    if not path.endswith('.py'): # static file
        try:
            if path == '/':
                path = '/index.html' # default page is the index.html
            with open('./static'+path, 'rb') as f:
                body = f.read()
        except Exception:
            flag = False # not find
    else: # dynamic file
        if path == '/login.py':
            body = login().encode('utf-8')
        elif path == '/register.py':
            body = register().encode('utf-8')
        else:
            flag = False
        
    if flag:
        status = '200 OK'
    else:
        status = '404 NOT FOUND'
        body = '<h1>404, not found</h1>'.encode('utf-8')
    headers = [('Connection', 'Keep-Alive'), ('Content-Length', '%d'%len(body))]

    start_response(status, headers)
    # 返回的body必须是bytes类型
    return body