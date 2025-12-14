from s3_client import get_s3_client   


BUCKET_NAME = "data-aging-simulator-v01"

def create_bucket_if_not_exists(s3_client, bucket_name):
    existing_buckets = s3_client.list_buckets()
    bucket_names = [bucket['Name'] for bucket in existing_buckets['Buckets']]
    
    if bucket_name not in bucket_names:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")


# create_bucket_if_not_exists(get_s3_client(), BUCKET_NAME)

def list_buckets():
    s3 = get_s3_client()
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])

list_buckets()
