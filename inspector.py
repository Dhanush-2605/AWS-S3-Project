from datetime import datetime, timezone
from s3_client import get_s3_client
import os
from dotenv import load_dotenv
import json
from presigned_access import generate_presigned_url
load_dotenv()

BUCKET_NAME= os.getenv('BUCKET_NAME')


def inspect_data():
    s3= get_s3_client()
    res=s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='data/')
    if 'Contents' not in res:
        print("No objects found with prefix 'data/'")
        return
    # print(res["Contents"])
    for obj in res['Contents']:
        key=obj["Key"]
        last_modified=obj["LastModified"]
        age_days=(datetime.now(timezone.utc)-last_modified).days
    
        if age_days < 7:
            state = "HOT"
            next_action = f"Move to WARM in {7 - age_days} days"
        elif age_days < 30:
            state = "WARM"
            next_action = f"Move to COLD in {30 - age_days} days"
        elif age_days < 90:
            state = "COLD"
            next_action = f"EXPIRE in {90 - age_days} days"
        else:
            state = "EXPIRED"
            next_action = "Deleted by lifecycle rule"

        print("\n---------------------------")
        print(f"File: {key}")
        print(f"Age: {age_days} days")
        print(f"State: {state}")
        print(f"Next Action: {next_action}")
        if state == "HOT":
            access = "Direct S3 access"
            # access=generate_presigned_url(key, 60)
        elif state == "WARM":
            access = generate_presigned_url(key, 300)   # 5 minutes
        elif state == "COLD":
            access = generate_presigned_url(key, 60)    # 1 minute
        else:
            access = "Access denied (expired)"

        print(f"Access: {access}")




inspect_data()



