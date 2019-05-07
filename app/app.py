#coding: utf-8
import face_recognition
from flask import Flask, jsonify, request, redirect, abort, Response
from flask_cors import CORS

import os
import os.path
from PIL import Image, ImageDraw
import base64
import json
from io import BytesIO
import re
import numpy as np
import tensorflow as tf
import time
import hmac
import logging
import redis
import find_face_save
import face_keras

from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m-%d-%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, filename='flask.log',
                    datefmt=DATE_FORMAT, format=LOG_FORMAT)  # 从debug输出

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'JPG'}

# 上传图片保存路径
PIC_PATH = 'pic/'
SAVE_FACE_PATH = 'face_pic/'

app = Flask(__name__, static_url_path='', static_folder='dist')
CORS(app, supports_credentials=True)

#redis连接
r = redis.StrictRedis('localhost', port=6379, db=0)
#mongodb连接
conn = MongoClient('localhost', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建
user_face = db.user_face #使用test_set集合，没有则自动创建

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/user/info', methods=['GET', 'POST'])
def userInfo():
    token = request.headers.get('X-Token')
    user = r.get(token)
    data = {'data': {'roles': 'admin',
                     'name': str(user),
                     'avatar': '',
                     'introduction': '123'
                     }, 'code': 20000}
    return json.dumps(data)


@app.route('/user/logout', methods=['GET', 'POST'])
def logout():
    print(request.headers)
    token = request.headers.get('X-Token')
    print(token)
    r.delete(token)
    data = {'data': {
            'msg': '退出成功'
            }, 'code': 20000}
    return json.dumps(data)


@app.route('/user/faceAuth', methods=['GET', 'POST'])
def user_face_auth():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        base64_img = json.loads(request.get_data())['imgData']
        print(len(base64_img))
        res = []
        for i in range(len(base64_img)):
            base64_data = re.sub('^data:image/.+;base64,', '', base64_img[i])
            img = base64.b64decode(base64_data)
            img_data = BytesIO(img)
            im = Image.open(img_data)
            im = im.convert('RGB')
            imgArray = np.array(im)
            predict = predict_image(imgArray)
            if predict:
                res.extend(predict)
        b = set(res)  # {2, 3}
        if len(b) == 1 and len(res) >= 3:
            token = generate_token(list(b)[0])
            data = {
                'token': token,
                'user': list(b)[0],
                'success': True,
                'msg': '验证成功',
                'code': 20000
            }
            # 将token保存在redis中
            r.set(token, list(b)[0], ex=300)
            return json.dumps(data)
        else:
            data = {
                'success': False,
                'msg': '验证失败',
                'code': 20000
            }
            return json.dumps(data)
    # If no valid image file was uploaded, show the file upload form:
    data = {
        'success': False,
        'msg': '验证失败',
        'code': 20000
    }
    return json.dumps(data)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        base64_img = json.loads(request.get_data())['imgData']
        user = json.loads(request.get_data())['username']
        #判断用户名是否存在
        print(user_face.find({"user_name":user}).count())
        if user_face.find({"user_name":user}).count() > 0:
            data = {
                'success': False,
                'msg': '用户已存在',
                'code': 20000
            }
            return json.dumps(data)
        print(len(base64_img))
        #在MongoDB中使用sort()方法对数据进行排序，sort()方法可以通过参数指定排序的字段，并使用 1 和 -1 来指定排序的方式，其中 1 为升序，-1为降序。
        finds = user_face.find().sort([("id",-1)]).limit(1)
        uid = 0;
        if finds.count() > 0 :
            uid = finds[0]['id'] + 1;
        print(uid)
        user_info = {
            'id': uid,
            'user_name':user,
            'create_time':time.time(),
            'update_time':time.time()
        }
        user_face.insert_one(user_info)
        res = []
        for i in range(len(base64_img)):
            base64_data = re.sub('^data:image/.+;base64,', '', base64_img[i])
            img = base64.b64decode(base64_data)
            img_data = BytesIO(img)
            im = Image.open(img_data)
            im = im.convert('RGB')
            imgArray = np.array(im)
            faces = face_recognition.face_locations(imgArray)
            if len(faces) == 1:
                file_path = PIC_PATH+user+str(i)+'.png'
                with open(file_path, 'wb') as f:
                    f.write(img)
            find_face_save.save_face(file_path, SAVE_FACE_PATH, user, uid)
        face_keras.train_face()
    data = {
        'success': True,
        'msg': '操作成功',
        'code': 20000
    }
    return json.dumps(data)


def certify_token(key, token):
    r'''
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True
# 生成token


def generate_token(key, expire=10):
    r'''
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

# 验证脸部信息


def predict_image(image):
    model = tf.keras.models.load_model('model/face_model.h5')
    face_encode = face_recognition.face_encodings(image)
    result = []
    for j in range(len(face_encode)):
        predictions1 = model.predict(np.array(face_encode[j]).reshape(1, 128))
        print(predictions1)
        if np.max(predictions1[0]) > 0.90:
            print(np.argmax(predictions1[0]).dtype)
            pred_user = user_face.find_one({'id': int(np.argmax(predictions1[0]))})
            print('第%d张脸是%s' % (j+1, pred_user['user_name']))
            result.append(pred_user['user_name'])
    return result


@app.route('/error', methods=['GET', 'POST'])
def error():
    data = {'data': {
            'msg': '未验证或验证超时'
            }, 'code': 20000}
    return json.dumps(data)


@app.before_request  # 请求前
def process_request(*args, **kwargs):
    print(request.path)
    token = request.headers.get('X-Token')
    
    if request.path.startswith('/js/') or request.path.startswith('/css/') or request.path.startswith('/favicon/'):  
        return None  
    if request.path in ['/user/faceAuth', '/user/logout', '/sockjs-node/info', '/user/register', '/']:
        return None
    
    data = {'data': {
        'msg': '无效token'
        }, 'code': 50008}
    resp = Response(json.dumps(data))
    print(token)
    if not token :
         abort(resp)
    user = r.get(token)
    if not user:
        abort(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)