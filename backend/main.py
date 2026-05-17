from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import routes

app = FastAPI(title="Document Intelligence System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.get("/")
def root():
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "frontend" / "index.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return {
        "message": "System is running. Please create frontend/index.html in the project root."
    }
