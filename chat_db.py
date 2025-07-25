import aiosqlite
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DB_PATH = Path(os.getenv("DB_PATH", "my_chatbot.db"))

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                history TEXT
            )
        ''')
        await db.commit()

async def save_session(session_id, history):
    history_json = json.dumps(history)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT OR REPLACE INTO sessions (session_id, history)
            VALUES (?, ?)
        ''', (session_id, history_json))
        await db.commit()

async def load_session(session_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT history FROM sessions WHERE session_id = ?', (session_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None

