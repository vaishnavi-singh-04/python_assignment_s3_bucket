from fastapi import FastAPI
from app.health_check.ping import router as ping_router
from app.s3_bucket.routes.s3_route import router as s3_bucket_router


app = FastAPI(title="AWS S3 File Uploader", description="FastAPI app to manage AWS S3")


app.include_router(ping_router)
app.include_router(s3_bucket_router)
