import sqlite3
from pathlib import Path

data_dir = Path(__file__).parent / 'data'
DB_PATH = data_dir / 'svc.db'


def init_db():
    data_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS templates (id TEXT PRIMARY KEY, meta TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS sources (id TEXT PRIMARY KEY, type TEXT, template_id TEXT, meta TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS plans (id TEXT PRIMARY KEY, template_id TEXT, source_id TEXT, data TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, plan_id TEXT, status TEXT, artifact TEXT)')
    conn.commit()
    return conn
