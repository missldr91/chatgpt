"""SQLite database models"""
import sqlite3
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/db.sqlite")

def init_db():
    """Initialize database with tables"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    # Templates table
    c.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            theme_meta TEXT,
            layout_catalog TEXT
        )
    ''')
    
    # Sources table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            template_id TEXT,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pages TEXT,
            FOREIGN KEY (template_id) REFERENCES templates(id)
        )
    ''')
    
    # Plans table
    c.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id TEXT PRIMARY KEY,
            template_id TEXT,
            source_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            slides TEXT,
            FOREIGN KEY (template_id) REFERENCES templates(id),
            FOREIGN KEY (source_id) REFERENCES sources(id)
        )
    ''')
    
    # Jobs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            plan_id TEXT,
            status TEXT DEFAULT 'queued',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            artifact_url TEXT,
            preview_pngs TEXT,
            report TEXT,
            FOREIGN KEY (plan_id) REFERENCES plans(id)
        )
    ''')
    
    conn.commit()
    conn.close()

class DBManager:
    """Simple database manager for SQLite operations"""
    
    def __init__(self):
        init_db()
    
    def execute(self, query: str, params: tuple = ()) -> List[Any]:
        """Execute a query and return results"""
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, params)
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result
    
    def insert_template(self, template_id: str, theme_meta: Dict, layout_catalog: List[Dict]) -> None:
        """Insert a new template"""
        query = "INSERT INTO templates (id, theme_meta, layout_catalog) VALUES (?, ?, ?)"
        self.execute(query, (template_id, json.dumps(theme_meta), json.dumps(layout_catalog)))
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get template by ID"""
        query = "SELECT * FROM templates WHERE id = ?"
        result = self.execute(query, (template_id,))
        if result:
            row = result[0]
            return {
                "id": row["id"],
                "theme_meta": json.loads(row["theme_meta"]),
                "layout_catalog": json.loads(row["layout_catalog"])
            }
        return None
    
    def insert_source(self, source_id: str, template_id: str, doc_type: str, pages: List[Dict]) -> None:
        """Insert a new source document"""
        query = "INSERT INTO sources (id, template_id, type, pages) VALUES (?, ?, ?, ?)"
        self.execute(query, (source_id, template_id, doc_type, json.dumps(pages)))
    
    def get_source(self, source_id: str) -> Optional[Dict]:
        """Get source by ID"""
        query = "SELECT * FROM sources WHERE id = ?"
        result = self.execute(query, (source_id,))
        if result:
            row = result[0]
            return {
                "id": row["id"],
                "template_id": row["template_id"],
                "type": row["type"],
                "pages": json.loads(row["pages"])
            }
        return None
    
    def insert_plan(self, plan_id: str, template_id: str, source_id: str, slides: List[Dict]) -> None:
        """Insert a new transformation plan"""
        query = "INSERT INTO plans (id, template_id, source_id, slides) VALUES (?, ?, ?, ?)"
        self.execute(query, (plan_id, template_id, source_id, json.dumps(slides)))
    
    def get_plan(self, plan_id: str) -> Optional[Dict]:
        """Get plan by ID"""
        query = "SELECT * FROM plans WHERE id = ?"
        result = self.execute(query, (plan_id,))
        if result:
            row = result[0]
            return {
                "id": row["id"],
                "template_id": row["template_id"],
                "source_id": row["source_id"],
                "slides": json.loads(row["slides"])
            }
        return None
    
    def update_plan_slides(self, plan_id: str, slides: List[Dict]) -> None:
        """Update plan slides"""
        query = "UPDATE plans SET slides = ? WHERE id = ?"
        self.execute(query, (json.dumps(slides), plan_id))
    
    def insert_job(self, job_id: str, plan_id: str) -> None:
        """Insert a new job"""
        query = "INSERT INTO jobs (id, plan_id) VALUES (?, ?)"
        self.execute(query, (job_id, plan_id))
    
    def update_job(self, job_id: str, status: str, artifact_url: str = None, 
                   preview_pngs: List[str] = None, report: Dict = None) -> None:
        """Update job status and results"""
        query = """
            UPDATE jobs 
            SET status = ?, artifact_url = ?, preview_pngs = ?, report = ?, updated_at = ?
            WHERE id = ?
        """
        self.execute(query, (
            status,
            artifact_url,
            json.dumps(preview_pngs) if preview_pngs else None,
            json.dumps(report) if report else None,
            datetime.now().isoformat(),
            job_id
        ))
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get job by ID"""
        query = "SELECT * FROM jobs WHERE id = ?"
        result = self.execute(query, (job_id,))
        if result:
            row = result[0]
            return {
                "id": row["id"],
                "plan_id": row["plan_id"],
                "status": row["status"],
                "artifact_url": row["artifact_url"],
                "preview_pngs": json.loads(row["preview_pngs"]) if row["preview_pngs"] else None,
                "report": json.loads(row["report"]) if row["report"] else None
            }
        return None