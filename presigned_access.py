from s3_client import get_s3_client
import os
from dotenv import load_dotenv
load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME')

def generate_presigned_url(s3_key, expiration=3600):
    s3= get_s3_client()
    url=s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': s3_key
        },
        ExpiresIn=expiration
    )
    return url

