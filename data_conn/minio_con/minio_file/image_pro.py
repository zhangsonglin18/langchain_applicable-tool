from xmlrpc.client import ResponseError
import datetime
from data_conn.minio_con.minio_server import minioClient

##todo 从本地上传图片
def upload():
    buget = "pictures"
    for i in range(100):
        try:
            found = minioClient.bucket_exists(bucket_name = buget)
            print(found)
            #获取年月日
            dir_name_master = datetime.datetime.now().strftime("%Y-%m")
            dir_name_slave = datetime.datetime.now().strftime("%Y-%m-%d")
            #设置文件的年月日时分秒格式
            file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            minioClient.fput_object(buget, "news/" + dir_name_slave + "/" + str(i)  + ".jpg","D:\\langchain_applicable-doc\\images\\" + str(i)  + '.jpg')
            print("down")
        except:
            pass

def upload_coco():
    buget = "pictures"
    directory = 'D:/model/data_set/image/test2017/test2017/'
    filenames = get_filenames(directory)
    found = minioClient.bucket_exists(bucket_name=buget)
    print(found)
    num = 0
    for i in filenames:
        try:
            if num<= 10000:
                #获取年月日
                dir_name_slave = datetime.datetime.now().strftime("%Y-%m-%d")
                #设置文件的年月日时分秒格式
                num+=1
                minioClient.fput_object(buget, "coco/" + dir_name_slave + "/" + str(i),"D:/model/data_set/image/test2017/test2017/" + str(i))
                print("down")
        except:
            pass


from minio import Minio
from io import BytesIO
from PIL import Image


def view_image(minio_client, bucket_name, object_name):
    # 获取对象内容并转换为Pillow中的Image格式
    object_data = minio_client.get_object(bucket_name, object_name)
    image_data = object_data.read()
    image = Image.open(BytesIO(image_data))
    image.show()

def view_image1(minio_client,bucket_name,object_name):
    # 获取对象内容并转换为Pillow中的Image格式
    object_data = minio_client.get_object(bucket_name, object_name)
    image_data = object_data.read()
    image = Image.open(BytesIO(image_data))
    return image

def view_image2(minio_client,bucket_name,object_name):
    # 获取对象内容并转换为Pillow中的Image格式
    object_data = minio_client.get_object(bucket_name, object_name)
    image_data = object_data.read()
    image = Image.open(BytesIO(image_data))
    return image
import os
def get_filenames(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# 示例用法

if __name__ == '__main__':
    # buget = "pictures"
    # dir_name_slave = "2024-03-23"
    # object = "news/" + dir_name_slave + "/" + str(73)  + ".jpg"
    # view_image(minioClient, buget, object)
    upload_coco()
    # 使用例子
    # directory = 'D:/model/data_set/image/test2017/test2017/'
    # filenames = get_filenames(directory)
    # print(len(filenames))




