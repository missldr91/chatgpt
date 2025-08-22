'use client';

import React, { useState } from 'react';
import { useStore } from '@/lib/store';
import { executePlan, getJobStatus, downloadOutput } from '@/lib/api';
import { LayoutSelector } from './LayoutSelector';

export function PlanPreview() {
  const { source, plan, job, jobId, setJob, setLoading, setError } = useStore();
  const [polling, setPolling] = useState(false);
  
  if (!plan || !source) return null;
  
  const handleExport = async () => {
    setLoading(true);
    try {
      const { job_id } = await executePlan(plan.plan_id);
      setJob({ status: 'queued' }, job_id);
      
      // Start polling for job status
      setPolling(true);
      const interval = setInterval(async () => {
        try {
          const status = await getJobStatus(job_id);
          setJob(status, job_id);
          
          if (status.status === 'done' || status.status === 'error') {
            clearInterval(interval);
            setPolling(false);
            
            if (status.status === 'done') {
              // Auto-download
              window.open(downloadOutput(job_id), '_blank');
            }
          }
        } catch (error) {
          console.error('Polling error:', error);
        }
      }, 2000);
      
      // Stop polling after 60 seconds
      setTimeout(() => {
        clearInterval(interval);
        setPolling(false);
      }, 60000);
      
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to start export');
      setPolling(false);
    } finally {
      setLoading(false);
    }
  };
  
  const getSlideStatus = (slide: typeof plan.slides[0]) => {
    if (slide.issues.length === 0) return 'green';
    if (slide.issues.includes('low_fit')) return 'red';
    return 'yellow';
  };
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'green': return 'bg-green-500';
      case 'yellow': return 'bg-yellow-500';
      case 'red': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };
  
  const greens = plan.slides.filter(s => getSlideStatus(s) === 'green').length;
  const yellows = plan.slides.filter(s => getSlideStatus(s) === 'yellow').length;
  const reds = plan.slides.filter(s => getSlideStatus(s) === 'red').length;
  
  return (
    <div className="w-full max-w-6xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Step 3: Review & Adjust</h2>
      
      {/* Status Summary */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center space-x-6">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span>{greens} Perfect</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
            <span>{yellows} Issues</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
            <span>{reds} Poor Fit</span>
          </div>
        </div>
      </div>
      
      {/* Source Type Warning */}
      {source.type === 'pdf' && (
        <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded">
          <p className="text-sm text-yellow-800">
            ⚠️ <strong>PDF Source:</strong> Medium/low reliability. Layout inference may not be perfect.
          </p>
        </div>
      )}
      
      {/* Slide Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        {plan.slides.map((slide, idx) => {
          const status = getSlideStatus(slide);
          const sourcePage = source.pages[slide.idx];
          
          return (
            <div key={idx} className="border rounded-lg p-4 relative">
              {/* Status Badge */}
              <div className={`absolute top-2 right-2 w-8 h-8 ${getStatusColor(status)} rounded-full flex items-center justify-center text-white text-xs font-bold`}>
                {status === 'green' ? '✓' : slide.issues.length}
              </div>
              
              {/* Slide Info */}
              <h3 className="font-semibold mb-2">Slide {idx + 1}</h3>
              
              {/* Preview Placeholder */}
              <div className="h-32 bg-gray-100 rounded mb-3 flex items-center justify-center text-gray-400">
                <div className="text-center">
                  <div className="text-2xl mb-1">📄</div>
                  <div className="text-xs">
                    {sourcePage.signature.title && 'Title '}
                    {sourcePage.signature.bullets > 0 && `${sourcePage.signature.bullets} bullets `}
                    {sourcePage.signature.images > 0 && `${sourcePage.signature.images} images `}
                    {sourcePage.signature.table && 'Table'}
                  </div>
                </div>
              </div>
              
              {/* Layout Selector */}
              <LayoutSelector slide={slide} slideIndex={idx} />
              
              {/* Issues */}
              {slide.issues.length > 0 && (
                <div className="mt-2 text-xs text-red-600">
                  Issues: {slide.issues.join(', ')}
                </div>
              )}
              
              {/* Warnings */}
              {sourcePage.warnings.length > 0 && (
                <div className="mt-1 text-xs text-yellow-600">
                  ⚠️ {sourcePage.warnings.join(', ')}
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Export Section */}
      <div className="border-t pt-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">Export Presentation</h3>
            <p className="text-sm text-gray-600">
              Generate the final PPTX with your brand template
            </p>
          </div>
          
          <button
            onClick={handleExport}
            disabled={polling}
            className={`
              px-6 py-3 rounded-lg font-medium transition-colors
              ${polling 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 text-white'
              }
            `}
          >
            {polling ? 'Processing...' : 'Export PPTX'}
          </button>
        </div>
        
        {/* Job Status */}
        {job && (
          <div className="mt-4 p-4 bg-gray-50 rounded">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Export Status: {job.status}</p>
                {job.report && (
                  <p className="text-sm text-gray-600 mt-1">
                    ✓ {job.report.greens} successful, 
                    ⚠️ {job.report.yellows} with issues
                  </p>
                )}
              </div>
              
              {job.status === 'done' && jobId && (
                <a
                  href={downloadOutput(jobId)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Download PPTX
                </a>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}