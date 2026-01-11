# AWS S3 File Uploader (FastAPI)

This project provides a small FastAPI application that exposes simple APIs to manage AWS S3 buckets, folders, and files. It includes endpoints to list/create/delete buckets, create/delete folders, upload/delete/copy/move files, and a health check.


Tech stack
- Python 3.10+
- FastAPI
- boto3 (AWS S3 client)

Quickstart

1. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Provide AWS credentials (example `.env` file or environment variables):

```text
AWS_ACCESS_KEY_ID=YOUR_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET
AWS_REGION=ap-south-2
```

3. Run the app with Uvicorn

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open the interactive docs at http://localhost:8000/docs

API Reference

Base path: `/` (FastAPI app). S3 endpoints are under `/s3`.

Health check
- GET `/ping`
  - Response: `{"status": "alive"}`
  - See [app/health_check/ping.py](app/health_check/ping.py)

S3 endpoints (prefix `/s3`)

- GET `/s3/buckets`
  - Description: List all buckets for the configured AWS credentials.
  - Response: Raw AWS `list_buckets` response (JSON from boto3).


- POST `/s3/create-bucket`
  - Description: Create a new S3 bucket.
  - Body: JSON matching `CreateBucketRequest`:

```json
{
  "bucket_name": "my-unique-bucket-name"
}
```

  - Behavior: Bucket name validated (DNS rules). Returns the boto3 `create_bucket` response or raises HTTP errors when unavailable or duplicate.


- DELETE `/s3/bucket/{bucket_name}`
  - Description: Delete the named bucket.
  - Path param: `bucket_name` (string)
  - Notes: If bucket is not empty, returns 409 (BucketNotEmpty).


- POST `/s3/create-folder`
  - Description: Create a folder (implemented as an S3 object with a trailing `/`).
  - Body: `CreateFolderRequest`:

```json
{
  "bucket_name": "my-bucket",
  "folder_name": "test_folder"
}
```

- DELETE `/s3/delete-folder`
  - Description: Delete all objects under a folder prefix.
  - Body: same as `CreateFolderRequest`.

- POST `/s3/upload-file/{bucket_name}`
  - Description: Upload a file to a bucket. Supports optional `folder_name` form field.
  - Path param: `bucket_name`
  - Form fields:
    - `file` (multipart upload)
    - `folder_name` (optional, string)


  - Response: `{"message": "File '<name>' uploaded to bucket '<bucket>'."}`

- DELETE `/s3/delete-file/{bucket_name}`
  - Description: Delete a file from bucket (optionally within a folder).
  - Query params: `file_name` (required), `folder_name` (optional)


- POST `/s3/copy-file`
  - Description: Copy a file inside a bucket (source and destination may include folders).
  - Body: `CopyMoveFileRequest`:

```json
{
  "bucket_name": "my-bucket",
  "file_name": "report.pdf",
  "source_folder": "inbox",
  "destination_folder": "archive"
}
```

- POST `/s3/move-file`
  - Description: Copy then delete the source file (move semantics).
  - Body: same as `CopyMoveFileRequest`.


Implementation notes & behavior
- The FastAPI router is defined in [app/s3_bucket/routes/s3_route.py](app/s3_bucket/routes/s3_route.py) and uses dependency injection to obtain `s3Service`.
- Business logic is implemented in [app/s3_bucket/services/s3_service.py](app/s3_bucket/services/s3_service.py).
- S3 calls are made through `s3Repository` in [app/s3_bucket/repositories/s3_repository.py](app/s3_bucket/repositories/s3_repository.py) which wraps `boto3` client calls.
- `create-folder` writes an empty object with a trailing slash to emulate folders in S3. `delete-folder` lists objects with the prefix and deletes them.
- Errors from AWS `ClientError` are mapped to HTTP errors (404, 409, 403, 500) with clear messages.
- The AWS client config is in [app/core/config.py](app/core/config.py). The app reads `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` environment variables.

Security & Credentials
- This service uses direct AWS credentials. Do NOT commit credentials to source control.
- For local testing, you can use environment variables or a `.env` file (project uses `python-dotenv` in `app/core/config.py`).


Notes
- Run interactive docs: http://localhost:8000/docs
- The main FastAPI app is created in [app/main.py](app/main.py).


Files of interest
- [app/main.py](app/main.py)
- [app/health_check/ping.py](app/health_check/ping.py)
- [app/s3_bucket/routes/s3_route.py](app/s3_bucket/routes/s3_route.py)
- [app/s3_bucket/services/s3_service.py](app/s3_bucket/services/s3_service.py)
- [app/s3_bucket/repositories/s3_repository.py](app/s3_bucket/repositories/s3_repository.py)
- [app/s3_bucket/schemas/s3_request_schema.py](app/s3_bucket/schemas/s3_request_schema.py)
- [app/core/config.py](app/core/config.py)
