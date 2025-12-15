from datetime import datetime, timezone
from s3_client import get_s3_client
import os
from dotenv import load_dotenv
load_dotenv()  

BUCKET_NAME = os.getenv('BUCKET_NAME')

COST_MULTIPLIER = {
    "HOT": 1.0,
    "WARM": 0.7,
    "COLD": 0.2
}

def estimate_cost():
    s3 = get_s3_client()

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="data/"
    )

    if "Contents" not in response:
        print("No data to estimate")
        return

    total_cost = 0

    for obj in response["Contents"]:
        size_mb = obj["Size"] / (1024 * 1024)
        age_days = (datetime.now(timezone.utc) - obj["LastModified"]).days

        if age_days < 7:
            state = "HOT"
        elif age_days < 30:
            state = "WARM"
        elif age_days < 90:
            state = "COLD"
        else:
            continue

        cost = size_mb * COST_MULTIPLIER[state]
        total_cost += cost

    print(f"Estimated monthly storage cost index: {round(total_cost, 2)}")
    print("(Lower is better due to lifecycle optimization)")

estimate_cost()