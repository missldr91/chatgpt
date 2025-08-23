#!/usr/bin/env python3
"""Test script to debug upload issue"""
import sys
import os
sys.path.insert(0, '/home/user/webapp/app/svc')

from pathlib import Path
from app.parsers.template_parser import TemplateParser

# Test with the fixture file
fixture_path = Path("/home/user/webapp/app/svc/data/fixtures/templates/brand_simple.pptx")
print(f"Testing with file: {fixture_path}")
print(f"File exists: {fixture_path.exists()}")
print(f"File size: {fixture_path.stat().st_size if fixture_path.exists() else 'N/A'}")

if fixture_path.exists():
    try:
        parser = TemplateParser(fixture_path)
        result = parser.parse()
        print("✓ Parsing successful!")
        print(f"Template ID: {result['template_id']}")
        print(f"Layouts found: {len(result['layout_catalog'])}")
    except Exception as e:
        print(f"✗ Error parsing: {e}")
        import traceback
        traceback.print_exc()
else:
    print("✗ File not found!")