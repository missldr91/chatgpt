"""Storage management utilities"""
from pathlib import Path
from typing import Optional
import shutil
import magic
import hashlib

class StorageManager:
    """Manage file storage operations"""
    
    BASE_PATH = Path("data")
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        dirs = ["templates", "sources", "plans", "jobs", "fixtures"]
        for dir_name in dirs:
            (cls.BASE_PATH / dir_name).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def save_template(cls, file_content: bytes, template_id: str) -> Path:
        """Save template file"""
        path = cls.BASE_PATH / "templates" / template_id / "template.pptx"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file_content)
        return path
    
    @classmethod
    def save_source(cls, file_content: bytes, source_id: str, ext: str) -> Path:
        """Save source file"""
        path = cls.BASE_PATH / "sources" / source_id / f"source.{ext}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file_content)
        return path
    
    @classmethod
    def get_template_path(cls, template_id: str) -> Optional[Path]:
        """Get template file path"""
        path = cls.BASE_PATH / "templates" / template_id / "template.pptx"
        return path if path.exists() else None
    
    @classmethod
    def get_source_path(cls, source_id: str) -> Optional[Path]:
        """Get source file path"""
        for ext in ["pptx", "pdf"]:
            path = cls.BASE_PATH / "sources" / source_id / f"source.{ext}"
            if path.exists():
                return path
        return None
    
    @classmethod
    def save_plan(cls, plan_id: str, plan_data: dict) -> Path:
        """Save plan as JSON"""
        import json
        path = cls.BASE_PATH / "plans" / f"{plan_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(plan_data, indent=2))
        return path
    
    @classmethod
    def get_plan(cls, plan_id: str) -> Optional[dict]:
        """Load plan from JSON"""
        import json
        path = cls.BASE_PATH / "plans" / f"{plan_id}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None
    
    @classmethod
    def get_job_output_path(cls, job_id: str) -> Path:
        """Get job output file path"""
        return cls.BASE_PATH / "jobs" / job_id / "output.pptx"

def validate_file_type(file_content: bytes, expected_types: list) -> tuple[bool, str]:
    """Validate file type using magic bytes"""
    try:
        # Check magic bytes
        mime = magic.from_buffer(file_content, mime=True)
        
        type_map = {
            "pptx": ["application/vnd.openxmlformats-officedocument.presentationml.presentation",
                     "application/zip"],  # PPTX is a zip file
            "pdf": ["application/pdf"]
        }
        
        for expected in expected_types:
            if expected in type_map:
                if mime in type_map[expected]:
                    return True, expected
        
        # Additional check for PPTX (check for specific files in zip)
        if "pptx" in expected_types and mime == "application/zip":
            import zipfile
            import io
            try:
                with zipfile.ZipFile(io.BytesIO(file_content)) as zf:
                    if "ppt/presentation.xml" in zf.namelist():
                        return True, "pptx"
            except:
                pass
        
        return False, mime
    except Exception as e:
        return False, str(e)