import urllib.parse
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.config import settings
from backend.database.models import Base

def ensure_database_exists():
    """If using MySQL/XAMPP, ensures the database exists before connecting."""
    if "mysql" in settings.DATABASE_URL:
        try:
            parsed = urllib.parse.urlparse(settings.DATABASE_URL)
            db_name = parsed.path.lstrip("/")
            host = parsed.hostname or "localhost"
            port = parsed.port or 3306
            user = parsed.username or "root"
            password = parsed.password or ""

            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                charset="utf8mb4"
            )
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[!] Note: Database check encountered: {e}")

# Ensure DB exists
ensure_database_exists()

# Configure engine
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine_args = {
    "connect_args": connect_args,
    "echo": False
}

if not is_sqlite:
    engine_args.update({
        "pool_pre_ping": True,
        "pool_recycle": 3600
    })

engine = create_engine(settings.DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    ensure_database_exists()
    Base.metadata.create_all(bind=engine)
