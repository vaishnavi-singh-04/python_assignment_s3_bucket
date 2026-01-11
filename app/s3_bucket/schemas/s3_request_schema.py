from fastapi import UploadFile
from pydantic import BaseModel, Field

from app.core.enums import AWSRegion

class CreateBucketRequest( BaseModel):
    bucket_name: str = Field(
        ...,
        description="Name of the S3 bucket. Must be globally unique and DNS compliant."
    )
    # region: AWSRegion = Field(
    #     default=AWSRegion.us_east_1,
    #     description="AWS region where the bucket will be created (e.g., ap-south-1)."
    # )
    

class CreateFolderRequest(BaseModel):
    bucket_name:  str = Field(
        ...,
        description="Name of the S3 bucket"
    )
    folder_name: str = Field(
        ...,
        description="Name of the folder inside the s3 bucket"
    )
    

class DeleteFolderRequest(CreateFolderRequest):
    pass


class CopyMoveFileRequest(BaseModel):
    bucket_name: str = Field(
        ...,
        description="Name of the S3 bucket"
    )
    file_name: str = Field(
        ...,
        description="Name of the file to copy or move (e.g., report.pdf)"
    )
    source_folder: str | None = Field(
        default=None,
        description="Optional source folder (e.g., input_folder)"
    )
    destination_folder: str | None = Field(
        default=None,
        description="Optional destination folder (e.g., archive_folder)"
    )
