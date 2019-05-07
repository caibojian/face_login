# face_login

#### 介绍
本项目基于tensorflow机器学习，实现web端人脸识别登陆，人脸注册。

提供手机端页面(face_login_app)和网页端页面(vue_element-admin)。

用户注册后进行一次机器学习，将用户的面部特征加入到模型中。



![pc端登陆](https://gitee.com/caibojian/face_login/raw/23b96dc25b6eaeb9684d9fa9a53fe1c968eac61b/doc/WechatIMG152.jpeg)

![pc端注册](https://gitee.com/caibojian/face_login/raw/23b96dc25b6eaeb9684d9fa9a53fe1c968eac61b/doc/WechatIMG151.jpeg)

![移动端](https://gitee.com/caibojian/face_login/raw/23b96dc25b6eaeb9684d9fa9a53fe1c968eac61b/doc/WechatIMG148.jpeg)

![](https://gitee.com/caibojian/face_login/raw/23b96dc25b6eaeb9684d9fa9a53fe1c968eac61b/doc/WechatIMG147.jpeg)

#### 软件架构

1. tensorflow 	用于人脸识别的机器学习

2. vue	web端开发

3. redis 	保存token，因为方便失效

4. MongoDB 	保存人脸已编码的数据和用户信息

5. flask	用于开发web接口，和返回静态页面

6. [face_recognition](https://github.com/ageitgey/face_recognition)	人脸识别python库，可以从照片中识别人脸




#### 安装教程

1. 运行app

   配置app.py中redis和mongodb的地址和端口

   ```shell
   python app.py
   ```



#### 使用说明

1. app 文件夹中保存项目的核心代码，提供数据访问接口，返回网页，训练模型，生成模型，验证图片等

2. face_login_app 文件夹中保存移动端代码，使用weui+vue，build后的dist代码放入到APP的dist中

3. vue-element-admin 文件夹为网页边人脸识别登陆前端代码

   

#### 特别说明

1. 手机端访问摄像头需要https

2. 目前iPhone的页面显示还有问题

3. 每次注册时tensorflow都要进行一次全局训练

   


#### TODO

1. 解决苹果手机无法使用问题
2. 提高tensorflow的训练效率
3. 开发小程序端
4. 开发树莓派版人脸识别