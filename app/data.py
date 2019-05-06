#coding:utf-8
import numpy as np 
from pymongo import MongoClient

#mongodb连接
conn = MongoClient('localhost', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建
face_images = db.face_images #使用test_set集合，没有则自动创建

lables = []
datas = []
INPUT_NODE = 128
LATER1_NODE = 200
OUTPUT_NODE = 0
TRAIN_DATA_SIZE = 0
TEST_DATA_SIZE = 0
def generateds():
    get_out_put_node()
    train_x, train_y, test_x, test_y = np.array(datas),np.array(lables),np.array(datas),np.array(lables)
    return train_x, train_y, test_x, test_y
def get_out_put_node():
    for item in face_images.find():
        lables.append(item['user_id'])
        datas.append(item['face_encoding'])
    OUTPUT_NODE = len(set(lables))
    TRAIN_DATA_SIZE = len(lables)
    TEST_DATA_SIZE = len(lables)
    return OUTPUT_NODE, TRAIN_DATA_SIZE, TEST_DATA_SIZE

def main():
    generateds()
if __name__ == '__main__':
    main()