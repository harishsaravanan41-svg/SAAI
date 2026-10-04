import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.config import settings
from backend.database.session import init_db
from backend.routers import auth_router, chat_router, tools_router

from ai_model.qwen_client import qwen_orchestrator

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize database tables on startup
    init_db()
    # 2. Pre-load local Qwen 2.5 1.5B model into memory
    try:
        qwen_orchestrator._load_local_model()
    except Exception as e:
        print(f"[!] Warning loading local model: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API with Zero-Trust AI Tool Calling, Session Security, and PostgreSQL/MySQL Database for SACAS College Assistant.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend UI connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(tools_router.router)

# Mount Frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def serve_root():
    login_path = os.path.join(frontend_dir, "login.html")
    if os.path.exists(login_path):
        return FileResponse(login_path)
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/login")
def serve_login():
    login_path = os.path.join(frontend_dir, "login.html")
    if os.path.exists(login_path):
        return FileResponse(login_path)
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/chat")
def serve_chat():
    chat_path = os.path.join(frontend_dir, "chat.html")
    if os.path.exists(chat_path):
        return FileResponse(chat_path)
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "llm_model": settings.LLM_MODEL
    }
