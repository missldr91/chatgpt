# Deck Transformer Monorepo

This repository provides a minimal MVP that restyles a source deck (PPTX or PDF) into a provided PPTX brand template. It includes:

- **/app/svc** – FastAPI service implementing template/source ingestion, planning, layout swapping, execution and job tracking.
- **/app/web** – Next.js 14 client with basic upload and export flow.
- **/app/infra** – `docker-compose` setup for local development.

## Quick start

```bash
# install python deps
pip install -r app/svc/requirements.txt
# generate fixtures (optional)
python app/svc/fixtures/generate.py
# run service
uvicorn app/svc/main:app --reload
```

In another terminal:

```bash
cd app/web
npm install
npm run dev
```

The web app expects the service at `NEXT_PUBLIC_SVC_URL` (default `http://localhost:8000`).

For Docker based dev:

```bash
cd app/infra
docker-compose up --build
```

## Testing

```bash
PYTHONPATH=app/svc pytest app/svc/tests
```

## Limitations & next steps

- Text overflow, image placement and table splitting use very rough heuristics.
- PDF ingestion offers only basic text extraction; reliability is medium/low and OCR is not yet wired.
- Execution copies simple text and ignores advanced formatting, animations or charts.
- Authentication, AV scanning and persistent object storage are out of scope for this MVP.
