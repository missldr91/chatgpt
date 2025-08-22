'use client';

import React from 'react';
import { useStore } from '@/lib/store';
import { swapLayout } from '@/lib/api';
import type { SlideMapping, LayoutInfo } from '@/types';

interface Props {
  slide: SlideMapping;
  slideIndex: number;
}

export function LayoutSelector({ slide, slideIndex }: Props) {
  const { template, plan, setPlan, setLoading, setError } = useStore();
  
  if (!template || !plan) return null;
  
  const handleLayoutChange = async (layoutId: string) => {
    if (layoutId === slide.chosen_layout_id) return;
    
    setLoading(true);
    try {
      const updatedPlan = await swapLayout(plan.plan_id, slideIndex, layoutId);
      setPlan(updatedPlan);
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to swap layout');
    } finally {
      setLoading(false);
    }
  };
  
  const currentLayout = template.layout_catalog.find(
    l => l.layout_id === slide.chosen_layout_id
  );
  
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Layout:
      </label>
      
      <select
        value={slide.chosen_layout_id}
        onChange={(e) => handleLayoutChange(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {template.layout_catalog.map((layout) => (
          <option key={layout.layout_id} value={layout.layout_id}>
            {layout.name} 
            {layout.placeholders.bodies > 0 && ` (${layout.placeholders.bodies} text)`}
            {layout.placeholders.pictures > 0 && ` (${layout.placeholders.pictures} img)`}
            {layout.placeholders.table && ' (table)'}
          </option>
        ))}
      </select>
      
      <div className="text-xs text-gray-500">
        <p>Current: {currentLayout?.name}</p>
        <p>Score: {(slide.score * 100).toFixed(0)}%</p>
      </div>
    </div>
  );
}