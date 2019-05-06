#coding:utf-8
import numpy as np 
from pymongo import MongoClient

#mongodb连接
conn = MongoClient('localhost', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建
user_face = db.user_face #使用test_set集合，没有则自动创建

pred_user = user_face.find_one({'id': 0})
print(pred_user['user_name'])