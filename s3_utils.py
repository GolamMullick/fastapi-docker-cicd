import boto3

def get_s3_client():
    return boto3.client('s3')

def upload_file_to_s3(file_obj, bucket_name, key):
    s3 = get_s3_client()
    s3.upload_fileobj(file_obj, bucket_name, key)

def download_file_from_s3(bucket_name, key):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return obj['Body'].read()
