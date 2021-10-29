import os
import time
import json
from flask import Flask, request, url_for, session, redirect, render_template, make_response

from model import MyMongodb

# flask 全局对象
app = Flask(__name__)

# 数据库操作
mongo_db = MyMongodb()


# 首页
@app.route('/')
@app.route('/page/<int:page_id>')
def index(page_id=None):
    mongo_db.user_add()
    # mongodb.clear_coll_datas(db)  # 清空整个集合
    # 获取用户上一次提交用的 cookies 用户名
    username = request.cookies.get('username')
    pages = mongo_db.get_all_count()
    if not page_id:
        page_id = 1
    # 显示指定页面
    docs = mongo_db.get_many_docs(page_id)
    data = {
        'username': username,
        'pages': pages,
        'pageId': page_id
    }
    return render_template('index.html', docs=docs, data=data)


# login 登陆后台
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lstrip()
        password = request.form['password'].lstrip()  # 获得登陆参数
        if username == '' or password == '':
            # 去除非法提交
            error = '你提交的内容错误'
            return render_template('error.html', error=error)
        docs = mongo_db.user_login(username, password)  # 查询参数是否正确
        if docs:
            resp = redirect(url_for('admin'))
            USERLOGINID = '12F4DDF90FAC22BA621698BC2060CC95DBCCA523'
            resp.set_cookie('USERLOGINID', USERLOGINID)  # 存储 cookie
            resp.set_cookie('USERLOGINNAME', username)
            return resp
        else:
            return redirect(url_for('login'))
    else:
        # get 页面
        return render_template('login.html')


# 网站后台
@app.route('/xionzhi',methods=['POST', 'GET'])
def admin():
    USERLOGINID = request.cookies.get('USERLOGINID', default='', type=str)
    USERLOGINNAME = request.cookies.get('USERLOGINNAME', default='', type=str)
    username = request.cookies.get('username', default='', type=str)
    search_str = request.cookies.get('search_str', default='', type=str)
    login_string = USERLOGINID + ':' + USERLOGINNAME + ':' + username
    # 查询数据库
    doc_data = mongo_db.find_user_admin(USERLOGINNAME)
    if doc_data:
        if login_string == doc_data['USERLOGINID']:
            # 返回网站后台页
            return render_template('admin.html', search_str=search_str)
    return redirect(url_for('login'))


# 提交一次 储存一次
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # 获取表单数据 去除两空格
        content = request.form['content'].lstrip()
        name = request.form['name'].lstrip()
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        # 本地测试需要更改 ip 来源
        user_ip = request.remote_addr
        # user_ip = request.headers['X-Forwarded-For']  # nginx 反向代理后的真实ip
        user_header = request.headers['User-Agent']
        user_error = time.strftime("%Y%m%d", time.localtime())
        # 如果提交空 则返回错误页
        if content == '' or name == '':
            error = '你提交的内容错误'
            return render_template('error.html', error=error)
        # 设置提交上限
        if not mongo_db.user_insert_error(user_ip):
            error = '你的请求达到限制'
            return render_template('error.html', error=error)
        data = {
            'name': name,  # 用户名
            'content': content,  # 提交的内容
            'localtime': local_time,  # 标准时间
            'user_ip': user_ip,  # ip地址
            'user_headers': user_header,  # 请求头 设备信息
            'user_error': user_error
        }
        # 储存用户输入
        mongo_db.insert_one_doc(data)
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', name)  # 存储 cookie
        return resp
    else:
        error = '这不科学, 难道你是机器人?'
        return render_template('error.html', error=error)


# search
@app.route('/search', methods=['GET', 'POST'])
def search(search_str=None):
    if request.method == 'POST':  # 后台采用post 查询
        search_str = request.form['word'].lstrip()
        if search_str:
            docs = mongo_db.get_str_docs(search_str)
            data_list = []
            for doc in docs:
                data = {
                    'name': doc['name'],
                    'content': doc['content'],
                    'localtime': doc['localtime'],
                    'ip': doc['user_ip'],
                    'headers': doc['user_headers'],
                    'id': str(doc['_id'])
                }
                data_list.append(data)
            resp = make_response(json.dumps(data_list))
            resp.set_cookie('search_str', search_str)
            return resp
        else:
            pass
    else:  # 前台搜索使用 get
        search_str = request.args.get('word', default=None, type=str)  # 搜索字符
        if search_str:
            # 搜索查询留言 json返回
            docs = mongo_db.get_str_docs(search_str)
            data_list = []
            for doc in docs:
                data = {
                    'name': doc['name'],
                    'content': doc['content'],
                    'localtime': doc['localtime']
                }
                data_list.append(data)
            resp = make_response(json.dumps(data_list))
            resp.set_cookie('search_str', search_str)
            return resp
        else:
            searchstr = request.cookies.get('search_str')
            return render_template('search.html', searchstr=searchstr)


# about
@app.route('/about')
def about():
    username = request.cookies.get('username')
    data = {
        'username': username,
    }
    return render_template('about.html', data=data)


# delete message
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        del_msg_id = request.form['delid'].lstrip()
        if del_msg_id:
            # 执行删除 留言
            delete_wt = mongo_db.delete_msg(del_msg_id)
            return(delete_wt)
    else:
        return ''


# 404 错误页
@app.errorhandler(404)
def page_not_found(error=None):
    # error = '404 not found'
    username = request.cookies.get('username')
    data = {
        'username': username,
    }
    return render_template('404.html', error=error, data=data), 404


# flask run
if __name__ == '__main__':
    app.run(port=8080, debug=True)
