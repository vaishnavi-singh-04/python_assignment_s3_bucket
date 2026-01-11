from fastapi import Depends
from app.core.config import get_s3_client_credentials
from app.s3_bucket.repositories.s3_repository import s3Repository
from app.s3_bucket.services.s3_service import s3Service

def get_s3_service() -> s3Service:
    s3_client = get_s3_client_credentials()
    repo = s3Repository(s3_client=s3_client)
    return s3Service(repo)

class SessionDependency:
    pass

