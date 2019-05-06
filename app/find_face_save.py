# coding:utf-8
# 从照片中识别出脸部特征并将脸部图像保存下来
from PIL import Image
import face_recognition
import random
import time
import glob
import os
from pymongo import MongoClient

#mongodb连接
conn = MongoClient('localhost', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建
face_images = db.face_images #使用test_set集合，没有则自动创建

def save_face(pic_path, save_path, username, uid):
    image = face_recognition.load_image_file(pic_path)
    face_encode = face_recognition.face_encodings(image)
    print(face_encode[0].shape)
    if(len(face_encode) == 1):
        face_image = {
            'user_id': uid,
            'face_encoding':face_encode[0].tolist()
        }
        face_images.insert_one(face_image)
    # face_locations = face_recognition.face_locations(image)
    # for face_location in face_locations:
    #     t = time.time()
    #     face_name = random.randint(0, 10000)
    #     top, right, bottom, left = face_location
    #     face_image = image[top:bottom, left:right]
    #     pil_image = Image.fromarray(face_image)
    #     file_path = save_path + username +'/'
    #     if not os.path.isdir(file_path):
    #         os.makedirs(file_path)
    #     file_name = str(round(t * 1000))+'face'+str(face_name)+'.png'
    #     pil_image.save(open(file_path + file_name, 'wb'), 'png')
