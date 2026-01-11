import re
from app.s3_bucket.repositories.s3_repository import s3Repository
from app.utils.logging_config import get_logger
from fastapi import HTTPException, UploadFile
from botocore.exceptions import ClientError
from app.s3_bucket.schemas.s3_request_schema import CreateBucketRequest, CreateFolderRequest, DeleteFolderRequest

class s3Service:
    def __init__(self, s3_repository: s3Repository):
        self.s3_repository = s3_repository
        self.logger = get_logger(__name__)
    
    # Validation
    def _validate_bucket_name(self, bucket_name: str):
        pattern = r"^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]$"
        if not re.match(pattern, bucket_name):
            self.logger.info("Pattern Verified")
            raise HTTPException(
                status_code=400,
                detail="Invalid bucket name. Bucket names must be 3–63 characters, Use lowercase letters, numbers and hyphens only."
            )
    
    def _build_file_key(self, file_name: str, folder_name: str | None):
        if folder_name:
            return f"{folder_name.rstrip('/')}/{file_name}"
        return file_name


    # LIST BUCKETS
    def list_buckets(self):
        try:
            self.logger.info("Fetching all S3 buckets")
            return self.s3_repository.list_all_buckets()

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)

            if error_code == "AccessDenied":
                self.logger.error(f"{error_code}: Access denied while listing S3 buckets.", exc_info=True)
                raise HTTPException(
                    status_code=403,
                    detail="Access denied while listing S3 buckets."
                )
            self.logger.error(f"{error_code}: Failed to list S3 buckets.", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to list S3 buckets."
            )

        except Exception:
            self.logger.error(f"Unexpected error while listing S3 buckets.", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error while listing S3 buckets."
            )
    

    # CREATE BUCKETS
    def create_bucket(self, request:CreateBucketRequest):
        try:
            self.logger.info(f"Bucket Name {request.bucket_name} | Creating S3 Buckets")
            # Validation
            self._validate_bucket_name(bucket_name=request.bucket_name)
            
            self.logger.info("Bucket name validated")
            
            return self.s3_repository.create_bucket(request.bucket_name)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)

            if error_code == "BucketAlreadyExists":
                self.logger.error(f"{error_code}: S3 Bucket already exists. Please choose a different name.", exc_info=True)
                raise HTTPException(
                    status_code=409,
                    detail="Bucket name already exists. Please choose a different name."
                )

            if error_code == "BucketAlreadyOwnedByYou":
                self.logger.error(f"{error_code}: Bucket already exists in your account.", exc_info=True)
                raise HTTPException(
                    status_code=409,
                    detail="Bucket already exists in your account."
                )
        except Exception as e:
            self.logger.error("Failed to create a bucket")
            raise HTTPException(
                status_code=500,
                detail="Failed to create bucket."
            )
            
    # DELETE BUCKET
    def delete_bucket(self, bucket_name: str):
        try:
            self.logger.info("Deleting Bucket")
            return self.s3_repository.delete_bucket(bucket_name)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)

            if error_code == "NoSuchBucket":
                self.logger.error(f"{error_code}: Bucket does exists in your account.", exc_info=True)
                raise HTTPException(
                    status_code=404,
                    detail="Bucket does not exist in your account."
                )

            if error_code == "BucketNotEmpty":
                self.logger.error(f"{error_code}: Bucket is not empty. Delete contents first.", exc_info=True)
                raise HTTPException(
                    status_code=409,
                    detail="Bucket is not empty. Delete contents first."
                )
        except Exception as e:
            self.logger.error("Failed to delete bucket")
            raise HTTPException(
                status_code=500,
                detail="Failed to delete bucket."
            )
    
    
    # CREATE FOLDER 
    def create_folder(self, request: CreateFolderRequest):
        try:
            self.logger.info(f"Creating Folder with bucket {request.bucket_name} and folder {request.folder_name}")
            self.s3_repository.create_object(request.bucket_name, request.folder_name)
            self.logger.info(f"Folder '{request.folder_name}' created in bucket '{request.bucket_name}")
            return {
                "message": f"Folder '{request.folder_name}' created in bucket '{request.bucket_name}'."
            }

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)

            if error_code == "NoSuchBucket":
                self.logger.error(f"{error_code}: Bucket does not exists.", exc_info=True)
                raise HTTPException(
                    status_code=404,
                    detail="Bucket does not exist."
                )
        except Exception as e:
            self.logger.error("Failed to create folder")
            raise HTTPException(
                status_code=500,
                detail="Failed to create folder."
            )
    
    def delete_folder(self, request:DeleteFolderRequest):
        try:
            self.logger.info(f"Deleting Folder with bucket {request.bucket_name} and folder {request.folder_name}")
            self.s3_repository.delete_object(request.bucket_name, request.folder_name)
            self.logger.info(f"Deleted Folder with bucket {request.bucket_name} and folder {request.folder_name}")
            return {
                "message": f"Folder '{request.folder_name}' deleted from bucket '{request.bucket_name}'."
            }
            
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)

            if error_code == "NoSuchBucket":
                self.logger.error(f"{error_code}: Bucket does not exists.", exc_info=True)
                raise HTTPException(
                    status_code=404,
                    detail="Bucket does not exist."
                )
        except Exception as e:
            
            self.logger.error("Failed to delete folder")
            raise HTTPException(
                status_code=500,
                detail="Failed to delete folder."
            )

    # Upload Files
    def upload_file(self, bucket_name: str, file: UploadFile, folder_name: str | None):
        try:
            filename = file.filename
            self.logger.info(f"Uploading file '{filename}' to bucket '{bucket_name}'")
            
            if folder_name:
                folder_name = folder_name.rstrip("/")
                file_key = f"{folder_name}/{filename}"
            else:
                file_key = filename
            # Read file content as bytes
            file_content = file.file.read()
            self.s3_repository.upload_file(bucket_name, str(file_key), file_content)
            
            self.logger.info(f"File '{filename}' uploaded successfully to bucket '{bucket_name}'")
            return {"message": f"File '{filename}' uploaded to bucket '{bucket_name}'."}
        
        except ClientError as e:
            
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)
            
            if error_code == "NoSuchBucket":
                self.logger.error(f"{error_code}: Bucket does not exists.", exc_info=True)
                raise HTTPException(status_code=404, detail="Bucket does not exist.")
            
            self.logger.error(f"{error_code}: Failed to upload file.", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to upload file.")
        
        except Exception:
            self.logger.error("Unexpected error while uploading file", exc_info=True)
            raise HTTPException(status_code=500, detail="Unexpected error while uploading file.")
    
    def delete_file(self, bucket_name: str, file_name: str, folder_name: str | None = None):
        try:
            if folder_name:
                folder_name = folder_name.rstrip("/")
                file_key = f"{folder_name}/{file_name}"
            else:
                file_key = file_name

            self.logger.info(
                f"Deleting file '{file_key}' from bucket '{bucket_name}'"
            )

            self.s3_repository.delete_file(bucket_name, file_key)

            return {
                "message": f"File '{file_key}' deleted from bucket '{bucket_name}'."
            }

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)
            if error_code == "NoSuchBucket":
                self.logger.error(f"{error_code}: Bucket does not exists.", exc_info=True)
                raise HTTPException(404, "Bucket does not exist")

            if error_code == "NoSuchKey":
                self.logger.error(f"{error_code}: File does not exists.", exc_info=True)
                raise HTTPException(404, "File does not exist")

            self.logger.error(f"{error_code}: Failed to delete the file.", exc_info=True)
            raise HTTPException(500, "Failed to delete file")

    def copy_file(
    self,
    bucket_name: str,
    file_name: str,
    source_folder: str | None,
    destination_folder: str | None,
    ):
        try:
            source_key = self._build_file_key(file_name, source_folder)
            destination_key = self._build_file_key(file_name, destination_folder)

            self.logger.info(
                f"Copying file from '{source_key}' to '{destination_key}' in bucket '{bucket_name}'"
            )

            self.s3_repository.copy_file(
                bucket_name=bucket_name,
                source_key=source_key,
                destination_key=destination_key,
            )

            return {
                "message": "File copied successfully",
                "source_key": source_key,
                "destination_key": destination_key,
            }

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)

            if error_code == "NoSuchBucket":
                raise HTTPException(404, "Bucket does not exist")

            if error_code == "NoSuchKey":
                raise HTTPException(404, "Source file does not exist")

            raise HTTPException(500, "Failed to copy file")

    def move_file(
    self,
    bucket_name: str,
    file_name: str,
    source_folder: str | None,
    destination_folder: str | None,
    ):
        try:
            source_key = self._build_file_key(file_name, source_folder)
            destination_key = self._build_file_key(file_name, destination_folder)

            self.logger.info(
                f"Moving file from '{source_key}' to '{destination_key}' in bucket '{bucket_name}'"
            )

            # Step 1: Copy
            self.s3_repository.copy_file(
                bucket_name=bucket_name,
                source_key=source_key,
                destination_key=destination_key,
            )

            # Step 2: Delete original (ONLY after successful copy)
            self.s3_repository.delete_file(bucket_name, source_key)

            return {
                "message": "File moved successfully",
                "source_key": source_key,
                "destination_key": destination_key,
            }

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            self.logger.error(f"Error Code: {error_code}", exc_info=True)

            if error_code == "NoSuchBucket":
                raise HTTPException(404, "Bucket does not exist")

            if error_code == "NoSuchKey":
                raise HTTPException(404, "Source file does not exist")

            raise HTTPException(500, "Failed to move file")
