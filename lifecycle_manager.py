import os
from s3_client import get_s3_client
from dotenv import load_dotenv
load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')

def apply_lifecycle_rules():
    s3 = get_s3_client()

    lifecycle_config = {
        "Rules": [
            {
                "ID": "LogsAndDataAging",
                "Status": "Enabled",
                "Filter": {
                    "Prefix": "data/"
                },
                "Transitions": [
                    {
                        "Days": 7,
                        "StorageClass": "INTELLIGENT_TIERING"
                    },
                    {
                        "Days": 30,
                        "StorageClass": "GLACIER"
                    }
                ],
                "Expiration": {
                    "Days": 90
                }
            }
        ]
    }

    s3.put_bucket_lifecycle_configuration(
        Bucket=BUCKET_NAME,
        LifecycleConfiguration=lifecycle_config
    )

    print("Lifecycle rules applied successfully")
    
apply_lifecycle_rules()