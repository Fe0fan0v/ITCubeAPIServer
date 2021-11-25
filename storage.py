import boto3
import os

ACCESS_ID = os.getenv('STORAGE_ACCESS_ID')
ACCESS_KEY = os.getenv('STORAGE_ACCESS_KEY')
IMAGE_BUCKET = os.getenv('IMAGE_BUCKET')

boto = boto3.client(
    's3',
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key=ACCESS_KEY,
    region_name='ru-central1',
    endpoint_url='https://storage.yandexcloud.net'
)


def upload(file_name, bucket_name, target_path):
    boto.upload_file(file_name, bucket_name, target_path)


def get_file_url(bucket_name, file_name):
    return f'https://storage.yandexcloud.net/{bucket_name}/{file_name}'
