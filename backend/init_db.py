"""Utility: create all tables. Run once to initialize a fresh database."""
import asyncio
from app.db.session import init_db

asyncio.run(init_db())
print("Tables created OK")
