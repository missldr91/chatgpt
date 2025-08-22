from typing import List, Dict, Any


def score_layout(sig: Dict[str, Any], layout: Dict[str, Any], theme: Dict[str, Any]):
    title_score = 1.0 if sig['title'] == layout['placeholders']['title'] else 0.0
    body_slots = layout['placeholders']['bodies']
    body_slot_score = min(1, body_slots/1)  # 1 if at least one body
    bullets_score = min(1, sig['bullets']/8) * body_slot_score
    columns_score = 1 if ((sig['columns']==2 and body_slots>=2) or (sig['columns']==1 and body_slots>=1)) else 0
    image_score = min(1, sig['images']/max(1, layout['placeholders']['pictures'])) if layout['placeholders']['pictures'] else (1 if sig['images']==0 else 0)
    table_score = 1 if sig['table'] and layout['placeholders']['table'] else 0
    score = 0.35*title_score + 0.25*bullets_score + 0.20*columns_score + 0.15*image_score + 0.05*table_score
    issues = []
    overflow_penalty = 0.0
    if sig['bullets'] > 8:
        issues.append('overflow')
        overflow_penalty = 0.1
    score -= overflow_penalty
    return score, issues


def plan_slides(slides: List[Dict[str, Any]], template: Dict[str, Any]):
    result = []
    layouts = template['layout_catalog']
    for slide in slides:
        best = {'score': -1, 'layout_id': None, 'issues': []}
        for layout in layouts:
            s, issues = score_layout(slide['signature'], layout, template['theme_meta'])
            if s > best['score']:
                best = {'score': s, 'layout_id': layout['layout_id'], 'issues': issues}
        if best['score'] < 0.55:
            best['issues'].append('low_fit')
            # fallback to first layout
            best['layout_id'] = layouts[0]['layout_id']
        result.append({'idx': slide['idx'], 'chosen_layout_id': best['layout_id'], 'score': round(best['score'],2), 'issues': best['issues']})
    return result
