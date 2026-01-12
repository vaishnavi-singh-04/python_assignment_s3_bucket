from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.health_check.ping import router as ping_router
from app.s3_bucket.routes.s3_route import router as s3_bucket_router

app = FastAPI(
    title="AWS S3 File Uploader",
    description="FastAPI app to manage AWS S3"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping_router)
app.include_router(s3_bucket_router)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Mount the entire frontend as static
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    # Serve index.html from /static so relative paths work
    return FileResponse(FRONTEND_DIR / "index.html")
