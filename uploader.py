import os
from datetime import datetime
from dotenv import load_dotenv
from s3_client import get_s3_client

load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
def upload_file(file_path, data_type):
    s3 = get_s3_client()

    file_name = os.path.basename(file_path)
    s3_key = f"data/{data_type}/{file_name}"

    s3.upload_file(
        Filename=file_path,
        Bucket=BUCKET_NAME,
        Key=s3_key,
        ExtraArgs={
            "Metadata": {
                "data_type": data_type,
                "uploaded_at": datetime.utcnow().isoformat()
            },
            "Tagging": f"category={data_type}"
        }
    )

    print(f"Uploaded {file_name} as {data_type}")



# upload_file("sample.log","logs")

