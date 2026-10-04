# 🎓 Personalized AI College Assistant — SACAS (SAAI)

A production-ready College Assistant built with **FastAPI**, **Qwen 2.5 1.5B (Function Calling)**, **XAMPP MySQL**, and **Zero-Trust Identity Injection**.

---

## 📁 Clean Project Directory Structure

```text
SAAI/
├── ai_model/                     # 🧠 AI Brain & Qwen 2.5 1.5B Orchestration
│   ├── Qwen2.5-1.5B-Instruct/    # Local Qwen 2.5 1.5B Tokenizer & Configuration
│   ├── prompt_templates.py       # Zero-trust system prompt & study-plan rules
│   ├── qwen_client.py            # Qwen 2.5 1.5B multi-mode connector
│   ├── response_validator.py     # PII scrubber & anti-hallucination guard
│   └── tool_definitions.py       # Function calling schemas (zero-identity leak)
│
├── backend/                      # ⚙️ FastAPI Backend Core
│   ├── auth/                     # Authentication & Security
│   │   ├── dependencies.py       # JWT Bearer token validator & session extractor
│   │   ├── schemas.py            # LoginRequest & Token models
│   │   └── security.py           # Bcrypt password hashing & JWT encoding
│   ├── database/                 # Database Layer
│   │   ├── models.py             # SQLAlchemy models (Departments, Staff, Events, Results)
│   │   ├── repositories.py       # 5 Parameterized SQL tools + NOT_FOUND handlers
│   │   └── session.py            # XAMPP MySQL connection & auto-db creator
│   ├── routers/                  # API Endpoints
│   │   ├── auth_router.py        # POST /api/auth/login, GET /api/auth/me
│   │   ├── chat_router.py        # POST /api/chat (Main AI Chat endpoint)
│   │   └── tools_router.py       # GET /api/tools/*
│   ├── schemas/                  # Pydantic Schemas
│   │   └── chat.py               # ChatRequest & ChatResponse schemas
│   ├── config.py                 # Pydantic settings (.env parser)
│   ├── main.py                   # FastAPI app entrypoint & UI route server
│   └── tool_executor.py          # Session identity injector & SQL tool dispatcher
│
├── frontend/                     # 💻 Web UI
│   ├── login.html                # Student Login Interface (Auto-password 123456)
│   ├── chat.html                 # AI Assistant Chatbot (Markdown tables, chips, tool badges)
│   └── index.html                # Navigation router
│
├── database_scripts/             # 🗄️ Database Seeds & Schemas
│   ├── init.sql                  # Database Schema definition
│   └── seed_data.py              # XAMPP MySQL database seeder
│
├── tests/                        # 🧪 Verification Test Suites
│   ├── test_backend.py           # Comprehensive automated unit tests (9 suites)
│   └── test_live_connectivity.py # Live end-to-end conversational test runner
│
├── .env.example                  # Template configuration & MySQL credentials
├── requirements.txt              # Python dependencies
├── run.py                        # Root launcher script
└── README.md                     # Documentation
```

---

## 🚀 Quick Start Guide

### 1. Ensure XAMPP MySQL is Running
Start **Apache & MySQL** from your XAMPP Control Panel.

### 2. Seed Database (One-time)
```bash
python database_scripts/seed_data.py
```

### 3. Start the Server
```bash
python run.py
```

- **Login Page**: [`http://localhost:8000/login`](http://localhost:8000/login)
- **Chat Assistant**: [`http://localhost:8000/chat`](http://localhost:8000/chat)
- **Swagger API Documentation**: [`http://localhost:8000/docs`](http://localhost:8000/docs)

### 4. Run Automated Tests
```bash
python tests/test_backend.py
```

---

## 🔑 Login Credentials

| Role | Username (Register Number) | Password | Name |
| :--- | :--- | :--- | :--- |
| **Student** | `222311669` | `123456` | AADHITHYA R |
| **Student (Rank 1)** | `222311696` | `123456` | AMUDHAVARSHINI S |
| **Admin** | `admin` | `admin123` | College Administrator |
