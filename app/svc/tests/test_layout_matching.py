"""Tests for layout matching and scoring"""
import pytest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from app.transformers import TransformationPlanner

def create_test_template_data():
    """Create test template data"""
    return {
        "template_id": "test_template",
        "theme_meta": {
            "fonts": {"title": "Arial", "body": "Calibri"},
            "colors": {f"accent{i}": f"#00000{i}" for i in range(1, 7)},
            "page_size": {"w": 9144000, "h": 6858000}
        },
        "layout_catalog": [
            {
                "layout_id": "layout_0",
                "name": "Title Slide",
                "placeholders": {"title": True, "bodies": 1, "pictures": 0, "table": False}
            },
            {
                "layout_id": "layout_1",
                "name": "Title and Content",
                "placeholders": {"title": True, "bodies": 1, "pictures": 0, "table": False}
            },
            {
                "layout_id": "layout_2",
                "name": "Two Content",
                "placeholders": {"title": True, "bodies": 2, "pictures": 0, "table": False}
            },
            {
                "layout_id": "layout_3",
                "name": "Picture with Caption",
                "placeholders": {"title": True, "bodies": 1, "pictures": 1, "table": False}
            },
            {
                "layout_id": "layout_4",
                "name": "Table",
                "placeholders": {"title": True, "bodies": 0, "pictures": 0, "table": True}
            }
        ]
    }

def create_test_source_data():
    """Create test source data"""
    return {
        "source_id": "test_source",
        "type": "pptx",
        "pages": [
            {
                "idx": 0,
                "signature": {
                    "title": True,
                    "bullets": 0,
                    "columns": 1,
                    "images": 0,
                    "table": False,
                    "coverage": {"text": 0.2, "image": 0.0}
                },
                "warnings": []
            },
            {
                "idx": 1,
                "signature": {
                    "title": True,
                    "bullets": 5,
                    "columns": 1,
                    "images": 0,
                    "table": False,
                    "coverage": {"text": 0.5, "image": 0.0}
                },
                "warnings": []
            },
            {
                "idx": 2,
                "signature": {
                    "title": True,
                    "bullets": 4,
                    "columns": 2,
                    "images": 0,
                    "table": False,
                    "coverage": {"text": 0.6, "image": 0.0}
                },
                "warnings": []
            },
            {
                "idx": 3,
                "signature": {
                    "title": True,
                    "bullets": 2,
                    "columns": 1,
                    "images": 1,
                    "table": False,
                    "coverage": {"text": 0.3, "image": 0.4}
                },
                "warnings": []
            },
            {
                "idx": 4,
                "signature": {
                    "title": True,
                    "bullets": 0,
                    "columns": 1,
                    "images": 0,
                    "table": True,
                    "coverage": {"text": 0.1, "image": 0.0}
                },
                "warnings": []
            }
        ]
    }

def test_planner_init():
    """Test planner initialization"""
    template = create_test_template_data()
    source = create_test_source_data()
    
    planner = TransformationPlanner(template, source)
    assert planner.template == template
    assert planner.source == source
    assert planner.plan_id is not None

def test_create_plan():
    """Test plan creation"""
    template = create_test_template_data()
    source = create_test_source_data()
    
    planner = TransformationPlanner(template, source)
    plan = planner.create_plan()
    
    assert "plan_id" in plan
    assert "slides" in plan
    assert len(plan["slides"]) == len(source["pages"])
    
    for slide in plan["slides"]:
        assert "idx" in slide
        assert "chosen_layout_id" in slide
        assert "score" in slide
        assert "issues" in slide
        assert 0 <= slide["score"] <= 1

def test_layout_scoring():
    """Test layout scoring algorithm"""
    template = create_test_template_data()
    source = create_test_source_data()
    
    planner = TransformationPlanner(template, source)
    
    # Test title slide matching
    title_sig = source["pages"][0]["signature"]
    title_layout = template["layout_catalog"][0]
    score, issues = planner._score_layout(title_sig, title_layout)
    assert score > 0.5  # Should be a good match
    
    # Test bullet slide matching
    bullet_sig = source["pages"][1]["signature"]
    content_layout = template["layout_catalog"][1]
    score, issues = planner._score_layout(bullet_sig, content_layout)
    assert score > 0.5  # Should be a good match
    
    # Test two-column matching
    two_col_sig = source["pages"][2]["signature"]
    two_col_layout = template["layout_catalog"][2]
    score, issues = planner._score_layout(two_col_sig, two_col_layout)
    assert score > 0.6  # Should be a better match for two-column
    
    # Test image slide matching
    image_sig = source["pages"][3]["signature"]
    picture_layout = template["layout_catalog"][3]
    score, issues = planner._score_layout(image_sig, picture_layout)
    assert score > 0.5  # Should match picture layout
    
    # Test table slide matching
    table_sig = source["pages"][4]["signature"]
    table_layout = template["layout_catalog"][4]
    score, issues = planner._score_layout(table_sig, table_layout)
    assert score > 0.4  # Should have some match for table

def test_overflow_detection():
    """Test overflow detection"""
    template = create_test_template_data()
    source = create_test_source_data()
    
    # Modify source to have many bullets
    source["pages"][1]["signature"]["bullets"] = 15
    source["pages"][1]["signature"]["coverage"]["text"] = 0.8
    
    planner = TransformationPlanner(template, source)
    plan = planner.create_plan()
    
    # Check that overflow is detected
    slide_with_overflow = plan["slides"][1]
    assert "overflow" in slide_with_overflow["issues"]

def test_low_fit_detection():
    """Test low fit detection"""
    template = create_test_template_data()
    source = create_test_source_data()
    
    # Create a signature that doesn't match well
    source["pages"].append({
        "idx": 5,
        "signature": {
            "title": False,
            "bullets": 0,
            "columns": 3,  # Three columns - no matching layout
            "images": 5,    # Many images
            "table": True,  # And a table
            "coverage": {"text": 0.1, "image": 0.8}
        },
        "warnings": []
    })
    
    planner = TransformationPlanner(template, source)
    plan = planner.create_plan()
    
    # Check that low_fit is detected for the complex slide
    last_slide = plan["slides"][-1]
    assert "low_fit" in last_slide["issues"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])