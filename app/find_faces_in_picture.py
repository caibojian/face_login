#coding:utf-8
#从照片中识别出脸部特征并将脸部图像保存下来
from PIL import Image
import face_recognition
import os,shutil
import os.path
import random
import time
import glob
from face_recognition.face_recognition_cli import image_files_in_folder

train_dir = "/Users/caibojian/workspace_py/ml/image"

save_path = "/Users/caibojian/workspace_py/ml/mini_face/"
# for class_dir in os.listdir(train_dir):
#     print(class_dir)
            
#     if not os.path.isdir(os.path.join(train_dir, class_dir)):
#         continue

    # Loop through each training image for the current person
data_dir = train_dir + '/*'
files_list = glob.glob(data_dir)
for img_path in files_list:
    print(img_path)
    image = face_recognition.load_image_file(img_path)
    face_locations = face_recognition.face_locations(image)
    # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

    for face_location in face_locations:
        t = time.time()
        fice_name = random.randint(0,10000)
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        file_name = save_path+str(round(t * 1000))+'face'+str(fice_name)+'.png'
        pil_image.save(open(file_name, 'wb'), 'png')
            
def dellPic(pic_ath, save_path):

        