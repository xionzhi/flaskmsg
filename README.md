# 一个留言板

## 配置环境

- `config.py` 修改数据库地址 数据库名称

## 启动方法

* 上线方法 
    - `gunicorn -w 1 -b 127.0.0.1:8080 app:app`

* 调试启动
    - `python3 app.py` 本地端口8080 `debug=true`

## 后台登陆

- cookie
