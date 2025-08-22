# PPTX Brand Restyler MVP

## Overview
A full-stack application that restyles source presentations (PPTX/PDF) into a provided brand template by intelligently mapping content to template layouts while preserving brand consistency.

**GitHub Repository**: https://github.com/missldr91/chatgpt

## Features
- **Primary Path**: PPTX → PPTX transformation with high fidelity
- **Secondary Path**: PDF → PPTX with medium/low reliability warning
- **Smart Layout Matching**: Scores and maps source slides to best-fit template layouts
- **Overflow Handling**: Auto-splits overflowing content into continuation slides
- **Issue Tracking**: Per-slide warnings (overflow, low_fit, unsupported_chart, ocr_used)
- **Interactive Preview**: Swap layouts per slide before export

## Tech Stack
- **Frontend**: Next.js 14, TypeScript, React, zustand, react-dropzone, shadcn/ui
- **Backend**: Python 3.11, FastAPI, python-pptx, pdfplumber
- **Infrastructure**: Docker Compose, SQLite, filesystem storage

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker
```bash
cd app/infra
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

### Local Development

#### Backend Setup
```bash
cd app/svc
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd app/web
npm install
npm run dev
```

## API Endpoints

1. **POST /templates/ingest** - Upload brand template PPTX
   - Returns: template_id, theme metadata, layout catalog

2. **POST /sources/ingest** - Upload source document (PPTX/PDF)
   - Returns: source_id, page signatures with content analysis

3. **POST /transform/plan** - Generate transformation plan
   - Returns: plan_id, slide mappings with scores and issues

4. **POST /transform/execute** - Execute transformation
   - Returns: job_id for polling

5. **GET /jobs/{job_id}** - Check job status
   - Returns: status, download URL, preview PNGs, quality report

6. **POST /plans/{plan_id}/swap** - Swap layout for specific slide
   - Returns: updated plan

## Project Structure
```
/app
├── web/          # Next.js frontend
├── svc/          # FastAPI backend service
├── infra/        # Docker configuration
└── README.md
```

## Data Storage
- **SQLite**: IDs and metadata (`/svc/data/db.sqlite`)
- **Filesystem**: Templates, sources, outputs (`/svc/data/`)
- **Fixtures**: Sample templates and sources (`/svc/data/fixtures/`)

## Testing
```bash
# Backend tests
cd app/svc
pytest tests/

# Frontend tests
cd app/web
npm test
```

## Fixtures
Auto-generated sample files:
- `brand_simple.pptx` - Basic brand template with 5 layouts
- `mini_5slide.pptx` - Sample source presentation
- `mini_pdf_5page.pdf` - Sample PDF source

## Limitations & Next Steps

### Current Limitations
1. **PDF Parsing**: Medium reliability due to layout inference challenges
2. **Chart Support**: Charts are detected but not recreated (marked as unsupported)
3. **Image Quality**: Basic aspect ratio preservation, no smart cropping
4. **Table Splitting**: Simple column-based splitting for wide tables
5. **Preview Generation**: Server-side PNG generation is low-fidelity
6. **Storage**: Local filesystem, not cloud-ready
7. **OCR**: Optional, requires Tesseract installation

### Next Steps
1. **Cloud Storage**: Migrate to S3/GCS for scalability
2. **Advanced Layout Matching**: ML-based layout similarity scoring
3. **Chart Recreation**: Parse and recreate native PPTX charts
4. **Smart Image Handling**: Content-aware cropping and positioning
5. **Batch Processing**: Support multiple file transformations
6. **Caching**: Redis for template/plan caching
7. **Authentication**: Add user management and access control
8. **Export Formats**: Support direct PowerPoint Online integration

## Environment Variables
```bash
# Backend
CORS_ORIGINS=http://localhost:3000
MAX_FILE_SIZE_MB=50
ENABLE_OCR=false

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Considerations
- File type validation via magic bytes
- 50MB file size limit
- Sanitized file paths (no directory traversal)
- CORS restricted to frontend origin
- No code evaluation from user input

## License
MIT