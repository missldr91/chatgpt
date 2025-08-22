"""Pydantic schemas for API request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

# Template schemas
class ThemeMeta(BaseModel):
    fonts: Dict[str, str] = Field(description="Title and body font names")
    colors: Dict[str, str] = Field(description="Accent colors 1-6")
    page_size: Dict[str, float] = Field(description="Width and height in points")

class LayoutPlaceholder(BaseModel):
    title: Optional[bool] = None
    bodies: int = 0
    pictures: int = 0
    table: Optional[bool] = None

class LayoutInfo(BaseModel):
    layout_id: str
    name: str
    placeholders: LayoutPlaceholder
    bbox: Optional[Dict[str, Any]] = None

class TemplateIngestResponse(BaseModel):
    template_id: str
    theme_meta: ThemeMeta
    layout_catalog: List[LayoutInfo]

# Source schemas
class PageSignature(BaseModel):
    title: bool = False
    bullets: int = 0
    columns: int = 1
    images: int = 0
    table: bool = False
    coverage: Dict[str, float] = Field(default_factory=lambda: {"image": 0.0, "text": 0.0})

class PageInfo(BaseModel):
    idx: int
    signature: PageSignature
    warnings: List[str] = Field(default_factory=list)

class SourceIngestResponse(BaseModel):
    source_id: str
    type: Literal["pptx", "pdf"]
    pages: List[PageInfo]

# Plan schemas
class SlideMapping(BaseModel):
    idx: int
    chosen_layout_id: str
    score: float = Field(ge=0, le=1)
    issues: List[str] = Field(default_factory=list)

class PlanResponse(BaseModel):
    plan_id: str
    slides: List[SlideMapping]

class SwapRequest(BaseModel):
    idx: int
    layout_id: str

# Job schemas
class JobStatus(BaseModel):
    status: Literal["queued", "running", "done", "error"]
    artifact_url: Optional[str] = None
    preview_pngs: Optional[List[str]] = None
    report: Optional[Dict[str, Any]] = None

class ExecuteResponse(BaseModel):
    job_id: str

# Transform request schemas
class PlanRequest(BaseModel):
    template_id: str
    source_id: str