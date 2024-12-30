import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

s3 = boto3.client("s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
print("Connected to S3 successfully!")

bucket_name = "python-s3-demo-bucket"

def get_file_list():
    try:
        file_list = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in file_list:
            print("The bucket is empty.")
            return
        
        print(f"You have {file_list['KeyCount']} files on this bucket:")

        for i, file in enumerate(file_list["Contents"], start=1):
            print(f"{i}. {file['Key']}")

    except Exception as e:
        print(f"An error occured: {e}")
        
get_file_list()