from minio import Minio
from config.configs import Minio_HOST, Minio_ACCESS_KEY, Minio_SECRET_KEY

class MinioTools:
    def __init__(self):
        self.client = Minio(Minio_HOST,
                        access_key=Minio_ACCESS_KEY,
                        secret_key=Minio_SECRET_KEY,
                        secure=False)

    def lists_bucket(self, bucket):
        print(self.client.list_buckets())
        data = self.client.list_objects(bucket, recursive=True)
        objs = []
        if self.client.bucket_exists(bucket):
            for obj in data:
                objs.append(obj.object_name)
        return objs


if __name__ == '__main__':
    miniotool = MinioTools()
    s = miniotool.lists_bucket("pictures")
    print(s)
