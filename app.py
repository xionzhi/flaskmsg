import os
import time
from flask import Flask, request, url_for, session, redirect, render_template, escape, abort, make_response

from model import MyMongodb

# flask 全局对象
app = Flask(__name__)
# 加密随机字符串
app.secret_key = os.urandom(16)

# 数据库操作对象
mongodb = MyMongodb()
# 数据库连接对象
db = mongodb.get_db()


# 首页
@app.route('/')
@app.route('/page/<int:page_id>')
def index(page_id=None):
    # mongodb.clear_coll_datas(db)  # 清空整个集合
    # 获取用户上一次提交用的 cookies 用户名
    username = request.cookies.get('username')
    pages = mongodb.get_all_count(db)
    if page_id:
    	# 显示指定页面
        docs = mongodb.get_many_docs(db, page_id)
        data = {
            'username': username,
            'pages': pages,
            'pageId': page_id
        }
        return render_template('index.html', docs=docs, data=data)
    else:
    	# 访问首页 显示第一页
        page_id = 1
        docs = mongodb.get_many_docs(db, page_id)
        data = {
            'username': username,
            'pages': pages,
            'pageId': page_id
        }
        return render_template('index.html', docs=docs, data=data)


# 提交一次 储存一次
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # 获取表单数据 去除两空格
        content = request.form['content'].lstrip()
        name = request.form['name'].lstrip()
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        user_ip = request.remote_addr
        # user_ip = request.headers['X-Forwarded-For']  # nginx 反向代理后的真实ip
        user_header = request.headers['User-Agent']
        user_error = time.strftime("%Y%m%d", time.localtime())
        # 设置提交上限
        if not mongodb.user_insert_error(db, user_ip):
            error = '你的请求达到限制'
            return render_template('error.html', error=error)
        # 如果提交空 则返回错误页
        if content == '' or name == '':
            error = '你提交的内容错误'
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
        mongodb.insert_one_doc(db, data)
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', name)  # 存储 cookie
        return resp
    else:
        error = '这不科学, 难道你是机器人?'
        return render_template('error.html', error=error)


@app.route('/search/<search_str>')
def search(search_str):
	# 搜索查询 留言
    username = request.cookies.get('username')
    pages = mongodb.get_all_count(db)
    page_id = 0
    data = {
        'username': username,
        'pages': pages,
        'pageId': page_id
    }
    search_str = str(search_str)
    docs = mongodb.get_str_docs(db, search_str)
    return render_template('index.html', docs=docs, data=data)


# about
@app.route('/about')
def about():
	# 关于页面
    return render_template('about.html')


# contact
@app.route('/contact')
def contact():
	#  联系我们
    return '<h1>待完善的搜索功能，请尝试使用以下url</h1><h2>msg.xionzhi.com/search/search_str</h2>'


# 404 错误页
@app.errorhandler(404)
def page_not_found(error=None):
    # error = '404 not found'
    return render_template('404.html', error=error), 404


if __name__ == '__main__':
    app.run(debug=True)
