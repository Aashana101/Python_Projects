import os
import paramiko
import boto3
from datetime import datetime

def backup_to_remote_server(local_dir, remote_host, remote_dir, ssh_username, ssh_key_path):
    """
    Backup a directory to a remote server using SSH and SCP.

    Args:
        local_dir (str): Path to the local directory to be backed up.
        remote_host (str): Remote server hostname or IP address.
        remote_dir (str): Path to the destination directory on the remote server.
        ssh_username (str): SSH username for the remote server.
        ssh_key_path (str): Path to the SSH private key file.

    Returns:
        bool: True if backup is successful, False otherwise.
    """
    try:
        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to remote server
        ssh_key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
        ssh_client.connect(remote_host, username=ssh_username, pkey=ssh_key)

        # Use SCP to transfer files
        sftp = ssh_client.open_sftp()
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_dir)
                remote_path = os.path.join(remote_dir, relative_path)

                remote_dir_path = os.path.dirname(remote_path)
                try:
                    sftp.stat(remote_dir_path)
                except FileNotFoundError:
                    sftp.mkdir(remote_dir_path)

                sftp.put(local_path, remote_path)

        # Close connections
        sftp.close()
        ssh_client.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def backup_to_cloud_storage(local_dir, bucket_name, aws_access_key_id, aws_secret_access_key):
    """
    Backup a directory to AWS S3.

    Args:
        local_dir (str): Path to the local directory to be backed up.
        bucket_name (str): Name of the S3 bucket.
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.

    Returns:
        bool: True if backup is successful, False otherwise.
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Upload directory to S3 bucket
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                s3_key = os.path.relpath(local_file_path, local_dir)
                s3_client.upload_file(local_file_path, bucket_name, s3_key)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def generate_report(success, destination, backup_type):
    """
    Generate a report on the success or failure of the backup operation.

    Args:
        success (bool): Whether the backup was successful or not.
        destination (str): Destination information (e.g., remote server or cloud storage).
        backup_type (str): Type of backup operation (remote server or cloud storage).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Success" if success else "Failure"
    report = f"Backup Status: {status}\n"
    report += f"Timestamp: {timestamp}\n"
    report += f"Destination: {destination}\n"
    report += f"Backup Type: {backup_type}\n"
    
    with open("backup_report.txt", "w") as report_file:
        report_file.write(report)

if __name__ == "__main__":
    # Specify the source directory to be backed up
    source_directory = "/path/to/source/directory"

    # Specify the remote server details
    remote_host = "remote_host_ip_or_hostname"
    remote_dir = "/path/to/remote/directory"
    ssh_username = "ssh_username"
    ssh_key_path = "/path/to/ssh/private/key"

    # Specify the cloud storage details (AWS S3)
    bucket_name = "your_bucket_name"
    aws_access_key_id = "your_access_key_id"
    aws_secret_access_key = "your_secret_access_key"

    # Perform backup to remote server
    remote_backup_success = backup_to_remote_server(source_directory, remote_host, remote_dir, ssh_username, ssh_key_path)

    # Perform backup to cloud storage
    cloud_backup_success = backup_to_cloud_storage(source_directory, bucket_name, aws_access_key_id, aws_secret_access_key)

    # Generate and save the report for each backup
    generate_report(remote_backup_success, f"Remote Server: {remote_host}:{remote_dir}", "Remote Server")
    generate_report(cloud_backup_success, f"AWS S3 Bucket: {bucket_name}", "Cloud Storage")
