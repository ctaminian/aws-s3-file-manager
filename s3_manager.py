import boto3
from dotenv import load_dotenv
import os
from botocore.exceptions import ClientError

def main():
    load_dotenv()
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")
    s3 = boto3.client("s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    print("Connected to S3 successfully!")
    bucket_name = "python-s3-demo-bucket"
    get_file_list(s3, bucket_name)
    upload_file(s3, "C:/Users/ctami/OneDrive/Desktop/file3.txt", bucket_name, "file3.txt")
    download_file(s3, bucket_name, "file3.txt", "C:/Users/ctami/OneDrive/Desktop/test")
    delete_file(s3, bucket_name, "file3.txt")

def validate_inputs(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Please specify a valid {name}")

def get_file_list(s3, bucket_name):
    try:
        validate_inputs(bucket_name, "bucket name")
        file_list = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in file_list:
            print("The bucket is empty.")
            return
        print(f"You have {file_list['KeyCount']} files on this bucket:")
        for i, file in enumerate(file_list["Contents"], start=1):
            print(f"{i}. {file['Key']}")
    except ClientError as e:
        print(f"Error fetching file list: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def upload_file(s3, file_path, bucket_name, file_name):
    validate_inputs(bucket_name, "bucket name")
    validate_inputs(file_name, "file name")
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False
    try:
        s3.upload_file(file_path, bucket_name, file_name)
        print(f"File '{file_name}' uploaded to bucket '{bucket_name}' successfully.")
        return True
    except ClientError as e:
        print(f"Upload failed: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
        return False

def download_file(s3, bucket_name, file_name, destination_path=None):
    validate_inputs(bucket_name, "bucket name")
    validate_inputs(file_name, "file name")
    if destination_path is None:
        destination_path = os.path.join(os.getcwd(), file_name)
    elif os.path.isdir(destination_path):
        destination_path = os.path.join(destination_path, file_name)
    try:
        s3.download_file(bucket_name, file_name, destination_path)
        print(f"File '{file_name}' downloaded to '{destination_path}' successfully.")
        return True
    except ClientError as e:
        print(f"Download failed: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
        return False

def delete_file(s3, bucket_name, file_name):
    validate_inputs(bucket_name, "bucket name")
    validate_inputs(file_name, "file name")
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(f"File '{file_name}' deleted successfully from bucket '{bucket_name}'.")
    except ClientError as e:
        print(f"Delete failed: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
        return False

if __name__ == "__main__":
    main()