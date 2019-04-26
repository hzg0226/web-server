import time
import pymysql

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

# 执行sql，返回数据
def execute_sql(sql, params):
    conn = pymysql.connect(host='192.168.56.104', port=3306, database='stock_db', charset='utf8', user='root', password='123456')
    cs = conn.cursor()
    cs.execute(sql, params)
    return cs.fetchall()

@route('/index.html')
def index():
    with open('./templates/index.html', 'rb') as f:
        content = f.read().decode('utf-8')
	
    sql = 'select * from info;'
    params = []
    data = execute_sql(sql, params)
    tr_template = '''
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
            </td>
        </tr>
	'''
    haha = ''
    for info in data:
        haha += tr_template%(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[0])
    content = content.replace('{%content%}', haha)

    return content.encode('utf-8')

@route('/center.html')
def center():
    with open('./templates/center.html', 'rb') as f:
        content = f.read().decode('utf-8')
    
    sql = 'select code, short, chg, turnover, price, highs, note_info from info, focus where focus.info_id=info.id'
    params = []
    data = execute_sql(sql, params)
    tr_template = '''
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
            </td>
            <td>
                <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
            </td>
        </tr>
	'''
    haha = ''
    for info in data:
        haha += tr_template%(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[0], info[0])
    content = content.replace('{%content%}', haha)
    
    return content.encode('utf-8')

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
    except Exception as ret:
        print(ret)
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