#!/usr/bin/env python3
"""Test the full transformation flow"""
import sys
sys.path.insert(0, '/home/user/webapp/app/svc')

import requests
from pathlib import Path
import time

API_URL = "http://localhost:8000"

# Test files
template_file = Path("/home/user/webapp/app/svc/data/fixtures/templates/brand_simple.pptx")
source_file = Path("/home/user/webapp/app/svc/data/fixtures/sources/mini_5slide.pptx")

print("=== Testing Full Flow ===\n")

# 1. Upload template
print("1. Uploading template...")
with open(template_file, "rb") as f:
    response = requests.post(f"{API_URL}/templates/ingest", files={"file": f})
    if response.status_code != 200:
        print(f"✗ Template upload failed: {response.text}")
        sys.exit(1)
    template_data = response.json()
    template_id = template_data["template_id"]
    print(f"✓ Template uploaded: {template_id}")

# 2. Upload source
print("\n2. Uploading source...")
with open(source_file, "rb") as f:
    response = requests.post(f"{API_URL}/sources/ingest?template_id={template_id}", files={"file": f})
    if response.status_code != 200:
        print(f"✗ Source upload failed: {response.text}")
        sys.exit(1)
    source_data = response.json()
    source_id = source_data["source_id"]
    print(f"✓ Source uploaded: {source_id}")

# 3. Create plan
print("\n3. Creating transformation plan...")
response = requests.post(f"{API_URL}/transform/plan", json={
    "template_id": template_id,
    "source_id": source_id
})
if response.status_code != 200:
    print(f"✗ Plan creation failed: {response.text}")
    sys.exit(1)
plan_data = response.json()
plan_id = plan_data["plan_id"]
print(f"✓ Plan created: {plan_id}")
print(f"  Slides: {len(plan_data['slides'])}")

# 4. Execute transformation
print("\n4. Executing transformation...")
response = requests.post(f"{API_URL}/transform/execute", params={"plan_id": plan_id})
if response.status_code != 200:
    print(f"✗ Execute failed: {response.text}")
    sys.exit(1)
job_data = response.json()
job_id = job_data["job_id"]
print(f"✓ Job started: {job_id}")

# 5. Poll for completion
print("\n5. Waiting for job completion...")
for i in range(30):  # Wait up to 30 seconds
    response = requests.get(f"{API_URL}/jobs/{job_id}")
    if response.status_code != 200:
        print(f"✗ Job status failed: {response.text}")
        sys.exit(1)
    
    job_status = response.json()
    status = job_status["status"]
    print(f"  Status: {status}")
    
    if status == "done":
        print(f"✓ Job completed successfully!")
        if job_status.get("report"):
            print(f"  Report: {job_status['report']}")
        break
    elif status == "error":
        print(f"✗ Job failed!")
        break
    
    time.sleep(1)

print("\n=== Test Complete ===")