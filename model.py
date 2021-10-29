import re
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

from config import MONGO_URL, MONGO_DB


class MyMongodb(object):
    def __init__(self):
        self.client = MongoClient(MONGO_URL, connect=False)
        self.db = self.client[MONGO_DB]

    # 写入一条数据
    def insert_one_doc(self, doc):
        posts = self.db['message']
        if doc:
            posts.insert(doc)
        else:
            return None

    # 查询带关键字的数据
    def get_str_docs(self, search_str):
        if search_str:
            posts = self.db['message']
            docs = posts.find({'$or': [{"content": re.compile(search_str)}, {"name": re.compile(search_str)}]})
            return docs
        else:
            return None

    # 查询总数据条数
    def get_all_count(self):
        posts = self.db['message']
        count = posts.find().count()
        return count/5

    # 清空一个表格 集合
    def clear_coll_datas(self):
        posts = self.db['message']
        posts.remove({})

    # 查询5条数据
    def get_many_docs(self, page_id):
        posts = self.db['message']
        start = (page_id - 1) * 5
        end = 5
        # docs = posts.find().limit(end).skip(start).sort({'$_id': -1})
        docs = posts.find().sort([("_id", -1)]).limit(end).skip(start)
        return docs

    # 写入限制
    def user_insert_error(self, ip):
        now_time = time.strftime("%Y%m%d", time.localtime())
        posts = self.db['message']
        count = posts.find({'user_ip': ip, 'user_error': now_time}).count()
        if count >= 10:
            return False
        else:
            return True
    
    # 增加一位用户
    def user_add(self):
        posts = self.db['users']
        docs = posts.find_one({"username": "xionzhi"})
        if docs:
            pass
        else:
            user_info_dict = {
                'username': 'xionzhi',
                'password': 'xz123456',
            }
            posts.insert(user_info_dict)
    
    # 用户登录
    def user_login(self, username, password):
        posts = self.db['users']
        docs = posts.find_one({"username": username, "password": password})
        if docs:
            return True
        else:
            return False

    # 后台验证登陆
    def find_user_admin(self, username):
        posts = self.db['users']
        docs = posts.find_one({"username": username})
        if docs:
            return docs
        else:
            return None

    # 通过id 删除留言
    def delete_msg(self, msg_id):
        posts = self.db['message']
        docs = posts.remove({"_id": ObjectId(msg_id)})
        return str(docs['n'])
