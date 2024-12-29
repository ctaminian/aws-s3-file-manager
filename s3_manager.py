import boto3
from dotenv import load_dotenv
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

try:
    s3_client = boto3.client("s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    print("Connected to S3 successfully!")

except NoCredentialsError:
    print("Error: No credentials provided. Check your .env file.")
except PartialCredentialsError:
    print("Error: Incomplete credentials provided. Verify your .env file.")
except ClientError as e:
    print(f"Client error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")