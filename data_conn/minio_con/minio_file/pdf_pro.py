from data_conn.minio_con.minio_server import minioClient
from minio.error import S3Error
import os

def upload_object(bucket_name = "pdffile"):
    # 放置一个具有默认内容类型的文件，成功后将打印服务器计算出的etag标识符
    try:
        with open('D:\\model\\data_set\\flickr30kzhbbosontrain\\ImageSets\\flickr30kzhbbosontrain.txt', 'rb') as file_data:
            file_stat = os.stat('D:\\model\\data_set\\flickr30kzhbbosontrain\\ImageSets\\flickr30kzhbbosontrain.txt')
            print(minioClient.put_object(bucket_name, 'flickr30kzhbbosontrain.txt',
                                         file_data, file_stat.st_size))
        print("Sussess")
    except S3Error as err:
        print(err)

if __name__ == '__main__':
    bucket_name = "pdffile"
    upload_object()
    print("Sussess")