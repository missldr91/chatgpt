"""Transformation planner for layout matching"""
from typing import Dict, List, Any
import uuid

class TransformationPlanner:
    """Plan slide-to-layout mappings with scoring"""
    
    def __init__(self, template: Dict, source: Dict):
        self.template = template
        self.source = source
        self.plan_id = str(uuid.uuid4())
    
    def create_plan(self) -> Dict[str, Any]:
        """Create transformation plan by matching pages to layouts"""
        slides = []
        
        for page in self.source["pages"]:
            best_layout, score, issues = self._find_best_layout(page["signature"])
            
            slides.append({
                "idx": page["idx"],
                "chosen_layout_id": best_layout["layout_id"],
                "score": round(score, 2),
                "issues": issues
            })
        
        return {
            "plan_id": self.plan_id,
            "slides": slides
        }
    
    def _find_best_layout(self, signature: Dict) -> tuple[Dict, float, List[str]]:
        """Find best matching layout for a page signature"""
        best_layout = None
        best_score = 0
        issues = []
        
        for layout in self.template["layout_catalog"]:
            score, layout_issues = self._score_layout(signature, layout)
            
            if score > best_score:
                best_score = score
                best_layout = layout
                issues = layout_issues
        
        # Use default layout if no good match
        if best_score < 0.55:
            issues.append("low_fit")
            # Try to find a basic Title+Content layout as fallback
            for layout in self.template["layout_catalog"]:
                if "content" in layout["name"].lower() or layout["placeholders"]["bodies"] > 0:
                    best_layout = layout
                    break
        
        # If still no layout, use first one
        if not best_layout:
            best_layout = self.template["layout_catalog"][0]
        
        return best_layout, best_score, issues
    
    def _score_layout(self, signature: Dict, layout: Dict) -> tuple[float, List[str]]:
        """Score how well a layout matches a signature"""
        score = 0.0
        issues = []
        placeholders = layout["placeholders"]
        
        # Title matching (35%)
        if signature["title"] and placeholders.get("title"):
            score += 0.35
        elif signature["title"] and not placeholders.get("title"):
            score -= 0.1
        elif not signature["title"] and placeholders.get("title"):
            score += 0.1  # Can still use title placeholder
        
        # Bullet/body matching (25%)
        if signature["bullets"] > 0:
            # Normalize bullets to 0-1 range (cap at 8 bullets)
            bullet_score = min(1.0, signature["bullets"] / 8)
            
            # Check if layout has body slots
            if placeholders["bodies"] > 0:
                score += 0.25 * bullet_score
            else:
                score -= 0.1
        elif placeholders["bodies"] > 0:
            score += 0.15  # Layout has bodies, can be used for text
        
        # Column matching (20%)
        if signature["columns"] == 2 and placeholders["bodies"] >= 2:
            score += 0.20
        elif signature["columns"] == 1 and placeholders["bodies"] == 1:
            score += 0.20
        elif signature["columns"] == 2 and placeholders["bodies"] < 2:
            score -= 0.05
            issues.append("column_mismatch")
        
        # Image matching (15%)
        if signature["images"] > 0:
            if placeholders["pictures"] > 0:
                # Good if layout has picture slots
                image_match = min(1.0, signature["images"] / max(1, placeholders["pictures"]))
                score += 0.15 * image_match
            else:
                # Penalty if images but no picture slots
                score -= 0.05
                if signature["images"] > 1:
                    issues.append("no_picture_slots")
        elif placeholders["pictures"] > 0:
            # Small penalty for unused picture slots
            score -= 0.02
        
        # Table matching (5%)
        if signature["table"] and placeholders.get("table"):
            score += 0.05
        elif signature["table"] and not placeholders.get("table"):
            issues.append("no_table_support")
        
        # Overflow detection (penalty)
        overflow_penalty = self._estimate_overflow(signature, placeholders)
        if overflow_penalty > 0:
            score -= overflow_penalty
            issues.append("overflow")
        
        return max(0, min(1, score)), issues
    
    def _estimate_overflow(self, signature: Dict, placeholders: Dict) -> float:
        """Estimate if content will overflow"""
        # Simple heuristic: if many bullets and only one body slot
        if signature["bullets"] > 12 and placeholders["bodies"] <= 1:
            return 0.1
        
        # If high text coverage and limited body slots
        if signature["coverage"]["text"] > 0.7 and placeholders["bodies"] <= 1:
            return 0.05
        
        return 0.0
    
    def swap_layout(self, idx: int, new_layout_id: str) -> Dict[str, Any]:
        """Swap layout for a specific slide"""
        # This would be called after retrieving the plan from DB
        # For now, return a placeholder
        return {
            "plan_id": self.plan_id,
            "slides": []  # Would be updated slides
        }