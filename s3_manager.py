import os
import sys
import boto3
import customtkinter
from tkinter import messagebox
from tkinter import filedialog
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

    upload_button = customtkinter.CTkButton(top_frame, text="Upload File", fg_color="#248823", hover_color="#014422", command=lambda: select_file_to_upload(s3, bucket_name, output_textbox))
    upload_button.pack(side="left", padx=20, pady=20)

    download_button = customtkinter.CTkButton(top_frame, text="Download File", fg_color="#248823", hover_color="#014422", command=lambda: get_filename_for_download(s3, bucket_name, output_textbox))
    download_button.pack(side="left", padx=20, pady=20)

    delete_button = customtkinter.CTkButton(top_frame, text="Delete File", fg_color="#248823", hover_color="#014422", command=lambda: get_filename_for_deletion(s3, bucket_name, output_textbox))
    delete_button.pack(side="left", padx=20, pady=20)

    exit_button = customtkinter.CTkButton(top_frame, text="Exit", fg_color="#248823", hover_color="#014422", command=exit_program)
    exit_button.pack(side="left", padx=20, pady=20)

    app.mainloop()
 
def exit_program():
    print("Thank you for using the AWS S3 File Manager. Goodbye!")
    sys.exit()

def list_files(s3, bucket_name, output_textbox):
    output_textbox.delete("1.0", "end")
    output_textbox.insert("end", "You chose to list files in the bucket\n")
    output_textbox.insert("end", "Fetching files...\n")
    output_textbox.insert("end", "\n")
    try:
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
    output_textbox.insert("end", "\n")

# Verify the bucket exists
def verify_bucket(s3, bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        print(f"Error verifying bucket: {e.response['Error']['Message']}")
        return False

# When upload file button is clicked, call this function to open the windows dialog box to select a file
def select_file_to_upload(s3, bucket_name, output_textbox):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    file_name = os.path.basename(file_path)
    output_textbox.insert("end", f"uploading {file_name}...\n")
    upload_file(s3, file_path, bucket_name, file_name, output_textbox)

# Upload file. S3 client, file path, bucket and file name required
def upload_file(s3, file_path, bucket_name, file_name, output_textbox):
    try:
        s3.upload_file(file_path, bucket_name, file_name)
        output_textbox.insert("end", f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' successfully.\n")
        return True
    except ClientError as e:
        messagebox.showerror("Error", f"Upload failed: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        return False

# When download button is clicked...call this function to show the popup dialog box
def get_filename_for_download(s3, bucket_name, output_textbox):
    dialog = customtkinter.CTkInputDialog(text="Type in the filename to download:", title="Download a file", button_fg_color="#248823", button_hover_color="#014422")
    filename = dialog.get_input()
    if filename:
        confirm_and_download(s3, bucket_name, filename, output_textbox)

# When filename is confirmed not to be empty, we can call this function to confirm file download and actually calling ehe S3 download function
def confirm_and_download(s3, bucket_name, filename, output_textbox):
    confirm = messagebox.askyesno("Confirm Download", f"Do you want to download '{filename}'?")
    if confirm:
        downloaded = download_file(s3, bucket_name, filename, output_textbox)
        if downloaded:
            messagebox.showinfo("Success", f"'{filename}' downloaded successfully!")

# Download file. S3 client, bucket, file name required, destination path is optional
def download_file(s3, bucket_name, file_name, output_textbox):
    destination_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)
    try:
        s3.download_file(bucket_name, file_name, destination_path)
        output_textbox.insert("end", f"File '{file_name}' downloaded to '{destination_path}' successfully.")
        return True
    except ClientError as e:
        messagebox.showerror("Error", f"Download failed: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        return False

# When delete button is clicked...call this function to show the popup dialog box
def get_filename_for_deletion(s3, bucket_name, output_textbox):
    dialog = customtkinter.CTkInputDialog(text="Type in the filename to delete:", title="Delete a file", button_fg_color="#248823", button_hover_color="#014422")
    filename = dialog.get_input()
    if filename:
        confirm_and_delete(s3, bucket_name, filename, output_textbox)

# When filename is confirmed not to be empty, we can call this function to confirm file delete and actually calling ehe S3 delete function
def confirm_and_delete(s3, bucket_name, filename, output_textbox):
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{filename}'?")
    if confirm:
        deleted = delete_file(s3, bucket_name, filename, output_textbox)
        if deleted:
            messagebox.showinfo("Success", f"'{filename}' deleted successfully!")

# Delete file. S3 client, bucket and file name required
def delete_file(s3, bucket_name, file_name, output_textbox):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=file_name)
    if "Contents" not in response:
        messagebox.showerror("Error", f"File '{file_name}' does not exist in the bucket.")
        return False
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        output_textbox.insert("end", f"File '{file_name}' deleted successfully from bucket '{bucket_name}'.\n")
        return True
    except ClientError as e:
        messagebox.showerror("Error", f"Deletion failed: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    main()