"""PDF source document parser"""
import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTFigure, LTImage, LTChar
from typing import Dict, List, Any, Optional
import uuid
from pathlib import Path
import pytesseract
from PIL import Image
import io

class PDFParser:
    """Parse PDF to extract page signatures with medium/low reliability"""
    
    def __init__(self, file_path: Path, template_id: str, enable_ocr: bool = False):
        self.file_path = file_path
        self.template_id = template_id
        self.source_id = str(uuid.uuid4())
        self.enable_ocr = enable_ocr
    
    def parse(self) -> Dict[str, Any]:
        """Extract signatures from all pages"""
        pages = []
        
        with pdfplumber.open(self.file_path) as pdf:
            for idx, page in enumerate(pdf.pages):
                signature, warnings = self._analyze_page(page, idx)
                pages.append({
                    "idx": idx,
                    "signature": signature,
                    "warnings": warnings
                })
        
        return {
            "source_id": self.source_id,
            "type": "pdf",
            "pages": pages
        }
    
    def _analyze_page(self, page, page_idx: int) -> tuple[Dict[str, Any], List[str]]:
        """Analyze a single PDF page"""
        warnings = []
        signature = {
            "title": False,
            "bullets": 0,
            "columns": 1,
            "images": 0,
            "table": False,
            "coverage": {"image": 0.0, "text": 0.0}
        }
        
        # Extract text with coordinates
        text_blocks = []
        text = page.extract_text()
        
        # If no text found and OCR is enabled, try OCR
        if not text and self.enable_ocr:
            try:
                # Convert page to image for OCR
                pil_image = page.to_image(resolution=150).original
                text = pytesseract.image_to_string(pil_image)
                warnings.append("ocr_used")
            except Exception:
                warnings.append("ocr_failed")
        
        # Get page dimensions
        page_width = page.width
        page_height = page.height
        total_area = page_width * page_height
        
        # Extract text blocks with positions using pdfminer
        try:
            page_layout = list(extract_pages(str(self.file_path), page_numbers=[page_idx]))[0]
            
            max_font_size = 0
            title_y_threshold = page_height * 0.25
            text_area = 0
            image_area = 0
            
            for element in self._flatten_layout(page_layout):
                if isinstance(element, LTTextBox):
                    # Calculate text area
                    elem_area = (element.x1 - element.x0) * (element.y1 - element.y0)
                    text_area += elem_area
                    
                    # Store text block info
                    text_blocks.append({
                        'text': element.get_text(),
                        'x': element.x0,
                        'y': page_height - element.y1,  # Convert to top-down coordinates
                        'width': element.x1 - element.x0,
                        'height': element.y1 - element.y0,
                        'centroid': (element.x0 + element.x1) / 2
                    })
                    
                    # Check for title (largest font in top 25%)
                    if (page_height - element.y1) < title_y_threshold:
                        # Try to get font size from characters
                        for char in self._get_chars(element):
                            if hasattr(char, 'size') and char.size > max_font_size:
                                max_font_size = char.size
                                signature["title"] = True
                    
                    # Count bullets
                    for line in element.get_text().split('\n'):
                        line = line.strip()
                        if line and line[0] in ['•', '·', '-', '–', '*', '◦']:
                            signature["bullets"] += 1
                        # Check for consistent indentation (heuristic for bullets)
                        elif line and len(line) > 2 and line[:2] == '  ':
                            signature["bullets"] += 1
                
                elif isinstance(element, (LTFigure, LTImage)):
                    signature["images"] += 1
                    elem_area = (element.x1 - element.x0) * (element.y1 - element.y0)
                    image_area += elem_area
        
        except Exception as e:
            warnings.append(f"layout_extraction_error")
        
        # Detect columns
        if len(text_blocks) >= 2:
            # Cluster by x-position
            left_blocks = [b for b in text_blocks if b['centroid'] < page_width * 0.45]
            right_blocks = [b for b in text_blocks if b['centroid'] > page_width * 0.55]
            
            if left_blocks and right_blocks:
                signature["columns"] = 2
        
        # Try to detect tables (basic heuristic)
        if page.find_tables():
            signature["table"] = True
        
        # Calculate coverage
        if total_area > 0:
            signature["coverage"]["text"] = min(1.0, text_area / total_area)
            signature["coverage"]["image"] = min(1.0, image_area / total_area)
        
        # Add PDF reliability warning
        if "pdf_reliability" not in warnings:
            warnings.append("pdf_reliability_medium")
        
        return signature, warnings
    
    def _flatten_layout(self, layout):
        """Recursively flatten layout tree"""
        for element in layout:
            if hasattr(element, '__iter__'):
                yield from self._flatten_layout(element)
            else:
                yield element
    
    def _get_chars(self, text_box):
        """Extract characters from text box"""
        for element in self._flatten_layout(text_box):
            if isinstance(element, LTChar):
                yield element