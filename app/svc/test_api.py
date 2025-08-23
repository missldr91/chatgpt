#!/usr/bin/env python3
"""Test the full API flow"""
import sys
sys.path.insert(0, '/home/user/webapp/app/svc')

from app.main import app
from fastapi.testclient import TestClient
from pathlib import Path

client = TestClient(app)

# Test with fixture
fixture_path = Path("/home/user/webapp/app/svc/data/fixtures/templates/brand_simple.pptx")

with open(fixture_path, "rb") as f:
    response = client.post(
        "/templates/ingest",
        files={"file": ("template.pptx", f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
    )
    
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✓ Success! Template ID: {data['template_id']}")
    print(f"Layouts: {len(data['layout_catalog'])}")
else:
    print(f"✗ Error: {response.text}")
    if response.status_code == 500:
        print("\nChecking for detailed error...")
        print(response.text)