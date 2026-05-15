import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из корня проекта
load_dotenv()

def get_db_path():
    return os.getenv("DB_PATH", "langlog.db")

def get_timezone():
    return os.getenv("TIMEZONE", "UTC")