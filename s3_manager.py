import os
import sys
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

def main():

    # Load environment variables
    load_dotenv()

    # Load AWS credentials and region
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")

    # Connect to S3
    s3 = boto3.client("s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    print("Connected to S3 successfully!")

    # Specify the bucket name
    bucket_name = "python-s3-demo-bucket"

    # Load the main menu
    load_menu(s3, bucket_name)

    # Main actions (get, upload, download, delete)
    # download_file(s3, bucket_name, "file3.txt", "C:/Users/ctami/OneDrive/Desktop/test")
    # delete_file(s3, bucket_name, "file3.txt")

# Loads the main menu
def load_menu(s3, bucket_name):
    while True:
        print("============================================")
        print("             AWS S3 File Manager")
        print("============================================")
        print("Please choose an option:")
        print("1. List files in the bucket")
        print("2. Upload a file")
        print("3. Download a file")
        print("4. Delete a file")
        print("5. Exit")
        print("============================================")
        try:
            user_choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        match user_choice:
            case 1:
                print("You chose to list files in the bucket")
                print("Fetching files...")
                get_file_list(s3, bucket_name)
            case 2:
                print("You chose to upload files to the bucket")
                file_path = input("Please enter the local file path: ").strip()
                if not file_path:
                    print("File path cannot be empty. Returning to menu.")
                    continue
                file_name = input("Please enter the file name to save in the bucket: ").strip()
                if not file_name:
                    print("File name cannot be empty. Returning to menu.")
                    continue
                upload_file(s3, file_path, bucket_name, file_name)
            case 3:
                print("3")
            case 4:
                print("4")
            case 5:
                print("Thank you for using the AWS S3 File Manager. Goodbye!")
                sys.exit()
            case _:
                print("Invalid choice. Please enter a number between 1 and 5.")

# Validate string inputs
def validate_inputs(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Please specify a valid {name}")
    
# List files. S3 client and bucket name required
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

# Upload file. S3 client, file path, bucket and file name required
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
    
# Download file. S3 client, bucket, file name required, destination path is optional, if left blank file downloads to current directory
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

# Delete file. S3 client, bucket and file name required
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