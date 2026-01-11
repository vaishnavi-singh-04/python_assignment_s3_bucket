from typing import Any
from app.utils.logging_config import get_logger

class s3Repository:
    def __init__(self, s3_client):
        self.s3_client = s3_client
        self.logger = get_logger(__name__)
    
    # Bucket Operations
    def list_all_buckets(self):
        print(f"{__file__} | Getting Credentials")    
        return self.s3_client.list_buckets()
    

    def create_bucket(self, bucket_name: str):
        return self.s3_client.create_bucket(Bucket=bucket_name)

    
    def delete_bucket(self, bucket_name: str):
        return self.s3_client.delete_bucket(Bucket=bucket_name)
    
    # Folder Operations
    def create_object(self, bucket_name:str, folder_name: str):
        if not folder_name.endswith("/"):
            folder_name = f"{folder_name}/"
        return self.s3_client.put_object(Bucket=bucket_name, Key=folder_name)
    
            
    def delete_object(self, bucket_name: str, folder_name: str):
        response = self.s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=f"{folder_name}/"
        )

        for obj in response.get("Contents", []):
            self.s3_client.delete_object(
                Bucket=bucket_name,
                Key=obj["Key"]
            )

    # Upload File
    def upload_file(self, bucket_name:str, file_key: str, file_content:bytes):
        return self.s3_client.put_object(
            Bucket= bucket_name,
            Key=file_key,
            Body=file_content
        )

    def delete_file(self, bucket_name: str, file_key: str):
        return self.s3_client.delete_object(
            Bucket=bucket_name,
            Key=file_key
        )
        
    # Copy file
    def copy_file(
        self,
        bucket_name: str,
        source_key: str,
        destination_key: str,
    ):
        return self.s3_client.copy_object(
            Bucket=bucket_name,
            CopySource={
                "Bucket": bucket_name,
                "Key": source_key,
            },
            Key=destination_key,
        )
