import os
import sys
import boto3
import customtkinter
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

    # Verify bucket exists
    if not verify_bucket(s3, bucket_name):
        print(f"Bucket '{bucket_name}' does not exist or is inaccessible. Exiting.")
        sys.exit()

    # Create the UI
    customtkinter.set_appearance_mode("Dark")
    app = customtkinter.CTk()
    app.title("AWS S3 Manager")
    app.geometry("1000x900")

    frame = customtkinter.CTkFrame(app)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    top_frame = customtkinter.CTkFrame(frame, fg_color="#242424")
    top_frame.pack(padx=20, pady=20)

    title_label = customtkinter.CTkLabel(top_frame, text="AWS S3 File Manager", font=("Helvetica", 20))
    title_label.pack(padx=20, pady=10)

    usage_label = customtkinter.CTkLabel(top_frame, text="Please click on any of the buttons below to begin.", font=("Helvetica", 14))
    usage_label.pack(padx=20, pady=10)

    output_textbox = customtkinter.CTkTextbox(frame, width=900, height=900, border_spacing=20, font=("Helvetica", 14), fg_color="#1d1e1e")
    output_textbox.pack(padx=20, pady=20)

    list_button = customtkinter.CTkButton(top_frame, text="List Files", fg_color="#248823", hover_color="#014422", command=lambda: list_files(s3, bucket_name, output_textbox))
    list_button.pack(side="left", padx=20, pady=20)

    upload_button = customtkinter.CTkButton(top_frame, text="Upload File", fg_color="#248823", hover_color="#014422")
    upload_button.pack(side="left", padx=20, pady=20)

    download_button = customtkinter.CTkButton(top_frame, text="Download File", fg_color="#248823", hover_color="#014422")
    download_button.pack(side="left", padx=20, pady=20)

    delete_button = customtkinter.CTkButton(top_frame, text="Delete File", fg_color="#248823", hover_color="#014422")
    delete_button.pack(side="left", padx=20, pady=20)

    exit_button = customtkinter.CTkButton(top_frame, text="Exit", fg_color="#248823", hover_color="#014422", command=exit_program)
    exit_button.pack(side="left", padx=20, pady=20)

    app.mainloop()

def exit_program():
    print("Thank you for using the AWS S3 File Manager. Goodbye!")
    sys.exit()

def list_files(s3, bucket_name, output_textbox):
    output_textbox.insert("end", "You chose to list files in the bucket\n")
    output_textbox.insert("end", "Fetching files...\n")
    output_textbox.insert("end", "\n")
    try:
        validate_inputs(bucket_name, "bucket name")
        file_list = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in file_list:
            output_textbox.insert("end", "The bucket is empty.\n")
            return
        output_textbox.insert("end", f"You have {file_list['KeyCount']} files on this bucket:\n")
        for i, file in enumerate(file_list["Contents"], start=1):
            output_textbox.insert("end", f"{i}. {file['Key']}\n")
    except ClientError as e:
        print(f"Error fetching file list: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Verify the bucket exists
def verify_bucket(s3, bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        print(f"Error verifying bucket: {e.response['Error']['Message']}")
        return False

# Validate string inputs
def validate_inputs(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Please specify a valid {name}")

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
        print(f"An unexpected error occurred during the file upload: {e}")
        return False

# Download file. S3 client, bucket, file name required, destination path is optional
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
        print(f"An unexpected error occurred during the file download: {e}")
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
        print(f"An unexpected error occurred while deleting the file: {e}")
        return False

if __name__ == "__main__":
    main()