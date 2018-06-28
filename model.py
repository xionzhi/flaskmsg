import re
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

from config import MONGO_URL, MONGO_DB


class MyMongodb(object):
    # 建立mongodb的链接
    def get_db(self):
        client = MongoClient(MONGO_URL, connect=False)
        db = client[MONGO_DB]
        # 返回数据库对象
        return db

    # 写入一条数据
    def insert_one_doc(self, db, doc):
        posts = db['message']
        if doc:
            posts.insert(doc)
        else:
            return None

    # 查询带关键字的数据
    def get_str_docs(self, db, search_str):
        if search_str:
            posts = db['message']
            docs = posts.find({'$or': [{"content": re.compile(search_str)}, {"name": re.compile(search_str)}]})
            return docs
        else:
            return None

    # 查询总数据条数
    def get_all_count(self, db):
        posts = db['message']
        count = posts.find().count()
        return count/5

    # 清空一个表格 集合
    def clear_coll_datas(self, db):
        posts = db['message']
        posts.remove({})

    # 查询5条数据
    def get_many_docs(self, db, page_id):
        posts = db['message']
        start = (page_id - 1) * 5
        end = 5
        # docs = posts.find().limit(end).skip(start).sort({'$_id': -1})
        docs = posts.find().sort([("_id", -1)]).limit(end).skip(start)
        return docs

    # 写入限制
    def user_insert_error(self, db, ip):
        now_time = time.strftime("%Y%m%d", time.localtime())
        posts = db['message']
        count = posts.find({'user_ip': ip, 'user_error': now_time}).count()
        if count >= 10:
            return False
        else:
            return True
    
    # 增加一位用户
    def user_add(self, db):
        posts = db['users']
        docs = posts.find_one({"username": "xionzhi"})
        if docs:
            pass
        else:
            user_info_dict = {
                'USERNAME': 'xionzhi',
                'PASSWORD': 'xz123456',
                'USERLOGINID': '12F4DDF90FAC22BA621698BC2060CC95DBCCA523'
            }
            posts.insert(user_info_dict)
    
    # 用户登录
    def user_login(self, db, username, password):
        posts = db['users']
        docs = posts.find_one({"username": username, "password": password})
        if docs:
            return True
        else:
            return False

    # 后台验证登陆
    def find_user_admin(self, db, username):
        posts = db['users']
        docs = posts.find_one({"username": username})
        if docs:
            return docs
        else:
            return None

    # 通过id 删除留言
    def delete_msg(self, db, msg_id):
        posts = db['message']
        docs = posts.remove({"_id": ObjectId(msg_id)})
        return str(docs['n'])
