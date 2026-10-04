import os
import sys
import uvicorn

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

if __name__ == "__main__":
    print("=========================================================")
    print("🎓 SAAI — S.A. ACADEMIC ARTIFICIAL INTELLIGENCE")
    print("=========================================================")
    print("🚀 Server URL:        http://localhost:8000")
    print("👉 Login Page:        http://localhost:8000/login")
    print("👉 Chat Interface:    http://localhost:8000/chat")
    print("👉 Swagger API Docs:  http://localhost:8000/docs")
    print("🔑 Default Password:  123456")
    print("=========================================================\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    reload_dirs = [
        os.path.join(base_dir, "backend"),
        os.path.join(base_dir, "ai_model"),
        os.path.join(base_dir, "frontend")
    ]
    reload_excludes = [
        "*.safetensors",
        "*.bin",
        "*.pt",
        "*.cache",
        "Qwen2.5-1.5B-Instruct/*"
    ]

    try:
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=reload_dirs,
            reload_excludes=reload_excludes
        )
    except KeyboardInterrupt:
        print("\n👋 SAAI Server stopped gracefully.")
