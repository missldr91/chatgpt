"""Main FastAPI application"""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import os
import asyncio
from pathlib import Path

from .models import DBManager
from .schemas import (
    TemplateIngestResponse, SourceIngestResponse, 
    PlanResponse, PlanRequest, SwapRequest,
    ExecuteResponse, JobStatus
)
from .parsers import TemplateParser, PPTXParser, PDFParser
from .transformers import TransformationPlanner, TransformationExecutor
from .utils import StorageManager, validate_file_type

# Initialize app
app = FastAPI(title="PPTX Restyler API", version="1.0.0")

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and storage
db = DBManager()
StorageManager.ensure_directories()

# File size limit (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "PPTX Restyler API"}

@app.post("/templates/ingest", response_model=TemplateIngestResponse)
async def ingest_template(file: UploadFile = File(...)):
    """Ingest a template PPTX file"""
    # Validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large. Maximum size is 50MB")
    
    # Validate file type
    is_valid, file_type = validate_file_type(content, ["pptx"])
    if not is_valid:
        raise HTTPException(400, f"Invalid file type. Expected PPTX, got {file_type}")
    
    # Parse template
    parser = TemplateParser(Path("temp.pptx"))  # Temporary workaround
    
    # Save file temporarily for parsing
    temp_path = Path("temp_template.pptx")
    temp_path.write_bytes(content)
    
    try:
        parser = TemplateParser(temp_path)
        result = parser.parse()
        
        # Save to storage
        template_id = result["template_id"]
        StorageManager.save_template(content, template_id)
        
        # Save to database
        db.insert_template(
            template_id,
            result["theme_meta"],
            result["layout_catalog"]
        )
        
        return result
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()

@app.post("/sources/ingest", response_model=SourceIngestResponse)
async def ingest_source(
    file: UploadFile = File(...),
    template_id: str = None
):
    """Ingest a source document (PPTX or PDF)"""
    if not template_id:
        raise HTTPException(400, "template_id is required")
    
    # Check template exists
    template = db.get_template(template_id)
    if not template:
        raise HTTPException(404, f"Template {template_id} not found")
    
    # Validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large. Maximum size is 50MB")
    
    # Validate file type
    is_valid, file_type = validate_file_type(content, ["pptx", "pdf"])
    if not is_valid:
        raise HTTPException(400, f"Invalid file type. Expected PPTX or PDF")
    
    # Save file temporarily for parsing
    ext = "pptx" if "pptx" in file_type or "presentation" in file_type else "pdf"
    temp_path = Path(f"temp_source.{ext}")
    temp_path.write_bytes(content)
    
    try:
        # Parse based on type
        if ext == "pptx":
            parser = PPTXParser(temp_path, template_id)
        else:
            parser = PDFParser(temp_path, template_id, enable_ocr=False)
        
        result = parser.parse()
        
        # Save to storage
        source_id = result["source_id"]
        StorageManager.save_source(content, source_id, ext)
        
        # Save to database
        db.insert_source(
            source_id,
            template_id,
            result["type"],
            result["pages"]
        )
        
        return result
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()

@app.post("/transform/plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest):
    """Create transformation plan"""
    # Get template and source from database
    template = db.get_template(request.template_id)
    if not template:
        raise HTTPException(404, f"Template {request.template_id} not found")
    
    source = db.get_source(request.source_id)
    if not source:
        raise HTTPException(404, f"Source {request.source_id} not found")
    
    # Create plan
    planner = TransformationPlanner(template, source)
    result = planner.create_plan()
    
    # Save to database
    db.insert_plan(
        result["plan_id"],
        request.template_id,
        request.source_id,
        result["slides"]
    )
    
    # Save to storage
    StorageManager.save_plan(result["plan_id"], result)
    
    return result

@app.post("/transform/execute", response_model=ExecuteResponse)
async def execute_transform(
    plan_id: str,
    background_tasks: BackgroundTasks
):
    """Execute transformation plan"""
    # Get plan from database
    plan = db.get_plan(plan_id)
    if not plan:
        raise HTTPException(404, f"Plan {plan_id} not found")
    
    # Create job
    import uuid
    job_id = str(uuid.uuid4())
    db.insert_job(job_id, plan_id)
    
    # Execute in background
    background_tasks.add_task(execute_job, job_id, plan)
    
    return {"job_id": job_id}

async def execute_job(job_id: str, plan: dict):
    """Background task to execute transformation"""
    try:
        db.update_job(job_id, "running")
        
        # Get paths
        template_path = StorageManager.get_template_path(plan["template_id"])
        source_path = StorageManager.get_source_path(plan["source_id"])
        
        if not template_path or not source_path:
            raise Exception("Template or source file not found")
        
        # Execute transformation
        executor = TransformationExecutor(plan, template_path, source_path)
        result = executor.execute()
        
        # Update job with results
        db.update_job(
            job_id,
            "done",
            result["artifact_url"],
            result["preview_pngs"],
            result["report"]
        )
    except Exception as e:
        db.update_job(job_id, "error")
        print(f"Job {job_id} failed: {e}")

@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get job status"""
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")
    
    return {
        "status": job["status"],
        "artifact_url": job["artifact_url"],
        "preview_pngs": job["preview_pngs"],
        "report": job["report"]
    }

@app.get("/jobs/{job_id}/download")
async def download_output(job_id: str):
    """Download job output file"""
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")
    
    if job["status"] != "done":
        raise HTTPException(400, f"Job {job_id} is not complete")
    
    output_path = StorageManager.get_job_output_path(job_id)
    if not output_path.exists():
        raise HTTPException(404, f"Output file not found")
    
    return FileResponse(
        str(output_path),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="transformed.pptx"
    )

@app.post("/plans/{plan_id}/swap", response_model=PlanResponse)
async def swap_layout(plan_id: str, request: SwapRequest):
    """Swap layout for a specific slide"""
    # Get plan from database
    plan = db.get_plan(plan_id)
    if not plan:
        raise HTTPException(404, f"Plan {plan_id} not found")
    
    # Update the specific slide's layout
    slides = plan["slides"]
    if request.idx < len(slides):
        slides[request.idx]["chosen_layout_id"] = request.layout_id
        
        # Recalculate score if needed (simplified for now)
        slides[request.idx]["score"] = 0.75
        
        # Update database
        db.update_plan_slides(plan_id, slides)
        
        # Update storage
        plan["slides"] = slides
        StorageManager.save_plan(plan_id, plan)
    
    return {
        "plan_id": plan_id,
        "slides": slides
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)