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

    #get_file_list(s3, bucket_name)
    #upload_file(s3, "C:/Users/ctami/OneDrive/Desktop/file2.txt", bucket_name, "file2.txt")
    #download_file(s3, bucket_name, "file2.txt", "C:/Users/ctami/OneDrive/Desktop/test")

def get_file_list(s3, bucket_name):
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

def upload_file(s3, file_path, bucket_name, file_name):
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("Please use a valid file path.")
    if not isinstance(bucket_name, str) or not bucket_name.strip():
        raise ValueError("Please specifity a bucket name.")
    if not isinstance(file_name, str) or not file_name.strip():
        raise ValueError("Please specifity a file name.")

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False
    
    else:
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

def download_file(s3, bucket_name, file_name, file_path=None):
    if file_path is None:
        file_path = os.path.join(os.getcwd(), file_name)
    else:
        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, file_name)

    if not isinstance(bucket_name, str) or not bucket_name.strip():
        raise ValueError("Please specifity a bucket name.")
    if not isinstance(file_name, str) or not file_name.strip():
        raise ValueError("Please specifity a file name.")

    else:
        try:
            s3.download_file(bucket_name, file_name, file_path)
            print(f"File '{file_name}' downloaded to '{file_path}' successfully.")
            return True
        except ClientError as e:
            print(f"Upload failed: {e.response['Error']['Message']}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during upload: {e}")
            return False

if __name__ == "__main__":
    main()