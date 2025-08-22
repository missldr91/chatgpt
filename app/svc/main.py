import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from db import init_db
from pptx_template import parse_template
from source_parser import parse_pptx, parse_pdf
from planner import plan_slides
from executor import execute

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

data_dir = Path(__file__).parent / 'data'
templates_dir = data_dir / 'templates'
sources_dir = data_dir / 'sources'
plans_dir = data_dir / 'plans'
jobs_dir = data_dir / 'jobs'
for d in [templates_dir, sources_dir, plans_dir, jobs_dir]:
    d.mkdir(parents=True, exist_ok=True)

conn = init_db()

class TemplateIngestResponse(BaseModel):
    template_id: str
    theme_meta: dict
    layout_catalog: list


@app.post('/templates/ingest', response_model=TemplateIngestResponse)
async def ingest_template(template: UploadFile = File(...)):
    template_id = str(uuid.uuid4())
    tpl_dir = templates_dir / template_id
    tpl_dir.mkdir(parents=True, exist_ok=True)
    tpl_path = tpl_dir / 'template.pptx'
    with tpl_path.open('wb') as f:
        f.write(await template.read())
    meta = parse_template(tpl_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO templates(id, meta) VALUES (?, ?)', (template_id, json.dumps(meta)))
    conn.commit()
    return TemplateIngestResponse(template_id=template_id, **meta)


class SourceIngestResponse(BaseModel):
    source_id: str
    type: str
    pages: list


@app.post('/sources/ingest', response_model=SourceIngestResponse)
async def ingest_source(template_id: str = Form(...), source: UploadFile = File(...)):
    source_id = str(uuid.uuid4())
    suffix = Path(source.filename).suffix.lower()
    src_dir = sources_dir / source_id
    src_dir.mkdir(parents=True, exist_ok=True)
    src_path = src_dir / f'source{suffix}'
    with src_path.open('wb') as f:
        f.write(await source.read())
    if suffix == '.pptx':
        pages = parse_pptx(src_path)
        src_type = 'pptx'
    else:
        pages = parse_pdf(src_path)
        src_type = 'pdf'
    cur = conn.cursor()
    cur.execute('INSERT INTO sources(id, type, template_id, meta) VALUES (?,?,?,?)', (source_id, src_type, template_id, json.dumps({'pages': pages})))
    conn.commit()
    return SourceIngestResponse(source_id=source_id, type=src_type, pages=pages)


class PlanRequest(BaseModel):
    template_id: str
    source_id: str

class PlanResponse(BaseModel):
    plan_id: str
    slides: list


@app.post('/transform/plan', response_model=PlanResponse)
async def create_plan(req: PlanRequest):
    cur = conn.cursor()
    tpl_row = cur.execute('SELECT meta FROM templates WHERE id=?', (req.template_id,)).fetchone()
    src_row = cur.execute('SELECT meta FROM sources WHERE id=?', (req.source_id,)).fetchone()
    if not tpl_row or not src_row:
        return JSONResponse(status_code=404, content={'error': 'template or source not found'})
    template_meta = json.loads(tpl_row[0])
    source_meta = json.loads(src_row[0])
    slides = plan_slides(source_meta['pages'], template_meta)
    plan_id = str(uuid.uuid4())
    plan = {'plan_id': plan_id, 'template_id': req.template_id, 'source_id': req.source_id, 'slides': slides}
    cur.execute('INSERT INTO plans(id, template_id, source_id, data) VALUES (?,?,?,?)', (plan_id, req.template_id, req.source_id, json.dumps(plan)))
    conn.commit()
    with (plans_dir / f'{plan_id}.json').open('w') as f:
        json.dump(plan, f)
    return PlanResponse(plan_id=plan_id, slides=slides)


class ExecuteRequest(BaseModel):
    plan_id: str

class ExecuteResponse(BaseModel):
    job_id: str


@app.post('/transform/execute', response_model=ExecuteResponse)
async def transform_execute(req: ExecuteRequest):
    cur = conn.cursor()
    plan_row = cur.execute('SELECT data FROM plans WHERE id=?', (req.plan_id,)).fetchone()
    if not plan_row:
        return JSONResponse(status_code=404, content={'error':'plan not found'})
    plan = json.loads(plan_row[0])
    template_path = templates_dir / plan['template_id'] / 'template.pptx'
    src_row = cur.execute('SELECT type FROM sources WHERE id=?', (plan['source_id'],)).fetchone()
    source_path = sources_dir / plan['source_id'] / ('source.pptx' if src_row and src_row[0]=='pptx' else 'source.pdf')
    job_id = str(uuid.uuid4())
    job_dir = jobs_dir / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    output_path = job_dir / 'output.pptx'
    execute(plan, template_path, source_path, output_path)
    cur.execute('INSERT INTO jobs(id, plan_id, status, artifact) VALUES (?,?,?,?)', (job_id, req.plan_id, 'done', str(output_path)))
    conn.commit()
    return ExecuteResponse(job_id=job_id)


class JobResponse(BaseModel):
    status: str
    artifact_url: str | None = None
    preview_pngs: list | None = None
    report: dict | None = None


@app.get('/jobs/{job_id}', response_model=JobResponse)
async def get_job(job_id: str):
    cur = conn.cursor()
    row = cur.execute('SELECT status, artifact FROM jobs WHERE id=?', (job_id,)).fetchone()
    if not row:
        return JSONResponse(status_code=404, content={'error':'job not found'})
    status, artifact = row
    artifact_url = str(Path('data') / 'jobs' / job_id / 'output.pptx') if artifact else None
    return JobResponse(status=status, artifact_url=artifact_url)


class SwapRequest(BaseModel):
    idx: int
    layout_id: int


@app.post('/plans/{plan_id}/swap', response_model=PlanResponse)
async def swap_layout(plan_id: str, req: SwapRequest):
    cur = conn.cursor()
    row = cur.execute('SELECT data FROM plans WHERE id=?', (plan_id,)).fetchone()
    if not row:
        return JSONResponse(status_code=404, content={'error':'plan not found'})
    plan = json.loads(row[0])
    for slide in plan['slides']:
        if slide['idx'] == req.idx:
            slide['chosen_layout_id'] = req.layout_id
            slide['issues'] = []
    cur.execute('UPDATE plans SET data=? WHERE id=?', (json.dumps(plan), plan_id))
    conn.commit()
    with (plans_dir / f'{plan_id}.json').open('w') as f:
        json.dump(plan, f)
    return PlanResponse(plan_id=plan_id, slides=plan['slides'])
