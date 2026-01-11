from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from app.core.session_dependencies import get_s3_service
from app.s3_bucket.repositories.s3_repository import s3Repository
from app.s3_bucket.schemas.s3_request_schema import CopyMoveFileRequest, CreateBucketRequest, CreateFolderRequest, DeleteFolderRequest
from app.s3_bucket.services.s3_service import s3Service

router = APIRouter(
    prefix="/s3",
    tags=["S3"]
)

# BUCKET ROUTES
@router.get("/buckets")
def list_buckets(service: s3Service = Depends(get_s3_service)):
    return service.list_buckets()

@router.post("/create-bucket")
def create_buckets(request: CreateBucketRequest,service: s3Service = Depends(get_s3_service)):
    return service.create_bucket(request)

@router.delete("/bucket/{bucket_name}")
def delete_bucket(bucket_name: str, service: s3Service = Depends(get_s3_service)):
    return service.delete_bucket(bucket_name= bucket_name)

# FOLDER ROUTES
@router.post("/create-folder")
def create_folder(
    request:CreateFolderRequest, service: s3Service = Depends(get_s3_service)
):
    return service.create_folder(request)

@router.delete("/delete-folder")
def delete_folder(
    request:DeleteFolderRequest, service: s3Service = Depends(get_s3_service)
):
    return service.delete_folder(request)


@router.post("/upload-file/{bucket_name}")
def upload_file(    
    bucket_name: str,
    folder_name : str | None = Form(
        None,
        description="Optional folder inside the bucket (e.g. test_folder)"
    ),
    file: UploadFile = File(..., description="The file to be uploaded to the S3 bucket. Supports any file type."),
    service: s3Service = Depends(get_s3_service)):
    return service.upload_file(bucket_name, file, folder_name)

# DELETE FILE
@router.delete("/delete-file/{bucket_name}")
def delete_file(
    bucket_name: str,
    file_name: str = Query(
        ...,
        description="Name of the file to delete (e.g. report.pdf)"
    ),
    folder_name: str | None = Query(
        None,
        description="Optional folder inside the bucket (e.g. test_folder)"
    ),
    service: s3Service = Depends(get_s3_service),
):
    return service.delete_file(bucket_name, file_name, folder_name)


# COPY FOLDER
@router.post("/copy-file")
def copy_file(
    request: CopyMoveFileRequest,
    service: s3Service = Depends(get_s3_service),
):
    return service.copy_file(
        bucket_name=request.bucket_name,
        file_name=request.file_name,
        source_folder=request.source_folder,
        destination_folder=request.destination_folder,
    )
    
@router.post("/move-file")
def move_file(
    request: CopyMoveFileRequest,
    service: s3Service = Depends(get_s3_service),
):
    return service.move_file(
        bucket_name=request.bucket_name,
        file_name=request.file_name,
        source_folder=request.source_folder,
        destination_folder=request.destination_folder,
    )

