import boto3

def read_content(bucket, mediafile_key):
    try:
        s3 = boto3.client('s3')
        data = s3.get_object(Bucket=bucket, Key=mediafile_key)

        content = data['Body'].read()
        return content

    except Exception as err:
        print(err)
        return None

def download_file(bucket, mediafile_key, local_path):
    try:
        s3 = boto3.client('s3')
        
        with open(local_path, 'wb') as file:
            s3.download_fileobj(bucket, mediafile_key, file)

        return local_path

    except Exception as err:
        print(err)
        return None

def put_file(bucket, mediafile_key, local_path):
    try:
        s3 = boto3.client('s3')
        s3.upload_file(local_path, bucket, mediafile_key)
        
        return True

    except Exception as err:
        print(err)
        return None

def put_object(bucket, mediafile_key, content):
    try:
        s3 = boto3.client('s3')
        
        s3.put_object(Bucket=bucket, Key=mediafile_key, Body=content)
        
        return True

    except Exception as err:
        print(err)
        return None


def upload_file(bucket, mediafile_key, local_path, content_type):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)

        return bucket.put_object(
            ACL='public-read',
            Body=open(local_path, 'rb'),
            ContentType=content_type,
            Key=mediafile_key
        )
    
    except Exception as err:
        print(err)
        return None        