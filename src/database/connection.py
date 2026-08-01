from sqlalchemy import create_engine
from src.database.config import *

DATABASE_URL=(
f"postgresql://"
f"{DB_USER}:{DB_PASSWORD}"
f"@{DB_HOST}:{DB_PORT}"
f"/{DB_NAME}"
)

engine=create_engine(DATABASE_URL)

def get_engine():
    return engine