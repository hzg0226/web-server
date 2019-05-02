import time
import pymysql
import re

# 路由字典，path-func
URL_FUNC = dict()
CONN = None
CS = None

# 路由装饰器
def route(url):
    def set_func(func):
        URL_FUNC[url] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func

# 使用数据库
def use_mysql(func):
    def call_func(*args, **kwargs):
        global CONN
        global CS
        CONN = pymysql.connect(host='192.168.56.104', port=3306, user='root', password='123456', database='stock_db', charset='utf8')
        CS = CONN.cursor()
        ret = func(*args, **kwargs)
        CS.close()
        CONN.close()
        return ret
    return call_func

@route(r'/index\.html')
@use_mysql
def index(ret):
    with open('./templates/index.html', 'rb') as f:
        content = f.read().decode('utf-8')
    
    # connect_to_mysql()

    sql = 'select * from info;'
    params = []
    CS.execute(sql, params)
    data = CS.fetchall()
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
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
            </td>
        </tr>
	'''
    haha = ''
    for info in data:
        haha += tr_template%(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[0])
    content = content.replace('{%content%}', haha)

    return content.encode('utf-8')

@route(r'/center\.html')
@use_mysql
def center(ret):
    with open('./templates/center.html', 'rb') as f:
        content = f.read().decode('utf-8')

    sql = 'select code, short, chg, turnover, price, highs, note_info from info, focus where focus.info_id=info.id'
    params = []
    CS.execute(sql, params)
    data = CS.fetchall()
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
                <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 无修改 </a>
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

@route(r'/login\.html')
def login(ret):
    return '<h1>login</h1>'.encode('utf-8')

@route(r'/register\.html')
def register(ret):
    return '<h1>register</h1>'.encode('utf-8')

@route(r'/add/(\d+)\.html')
@use_mysql
def add(ret):
    sql = 'select * from focus, info where focus.info_id=info.id and info.id=%s'
    params = [ret.group(1)]
    CS.execute(sql, params)
    data = CS.fetchall()
    if data:
        return 'already focused!'.encode('utf-8')
    else:
        sql = 'insert into focus values(default, "", %s)'
        try:
            CS.execute(sql, params)
        except Exception as ret:
            print(ret)
            CONN.rollback()
            return 'failed to add!'.encode('utf-8')
        else:
            CONN.commit()
            return 'add successfully!'.encode('utf-8')

@route(r'/delete/(\d+)\.html')
@use_mysql
def delete(ret):
    sql = 'delete from focus where info_id=(select id from info where code=%s)'
    params = [ret.group(1)]
    try:
        CS.execute(sql, params)
    except Exception:
        CONN.rollback()
        return 'failed to delete!'.encode('utf-8')
    else:
        CONN.commit()
        return 'delete successfully!'.encode('utf-8')

@route(r'/update/(\d+)\.html')
@use_mysql
def delete(ret):
    print(ret.group(1))
    with open('./templates/update.html', 'rb') as f:
        content = f.read().decode('utf-8')
    
    sql = 'select code, note_info from info, focus where info.id=focus.info_id and info.code=%s'
    params = [ret.group(1)]
    CS.execute(sql, params)
    code, info = CS.fetchone()
    
    content = content.replace('{%code%}', code)
    content = content.replace('{%note_info%}', info)
    return content.encode('utf-8')

@route(r'/update/(\d+)/(\w*)\.html')
@use_mysql
def delete(ret):
    print(ret.group(1), ret.group(2))
    
    sql = 'update focus set note_info=%s where info_id=(select id from info where code=%s)'
    params = [ret.group(2), ret.group(1)]
    try:
        CS.execute(sql, params)
    except Exception:
        CONN.rollback()
        return 'failed to update!'.encode('utf-8')
    else:
        CONN.commit()
        return 'update successfully!'.encode('utf-8')


def application(env, start_response):
    path = env['path']
    flag = True
    if path == '/':
        path = '/index.html' # default page is the index.html
    
    print(path)
    try:
        for url, func in URL_FUNC.items():
            ret = re.match(url, path)
            if ret:
                body = func(ret)
                break
        else:
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