'use client';

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useStore } from '@/lib/store';
import { uploadSource, createPlan } from '@/lib/api';

export function SourceUpload() {
  const { template, setSource, setPlan, setLoading, setError } = useStore();
  
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file || !template) return;
    
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext !== 'pptx' && ext !== 'pdf') {
      setError('Please upload a PPTX or PDF file');
      return;
    }
    
    setLoading(true);
    try {
      // Upload source
      const source = await uploadSource(file, template.template_id);
      setSource(source);
      
      // Create plan
      const plan = await createPlan(template.template_id, source.source_id);
      setPlan(plan);
      
      // Show PDF warning if needed
      if (source.type === 'pdf') {
        setTimeout(() => {
          alert('⚠️ PDF Import Notice: PDF to PPTX conversion has medium/low reliability. Some formatting may be lost.');
        }, 100);
      }
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to upload source');
    } finally {
      setLoading(false);
    }
  }, [template, setSource, setPlan, setLoading, setError]);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
  });
  
  if (!template) return null;
  
  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Step 2: Upload Source Document</h2>
      
      <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded">
        <p className="text-sm text-green-800">
          ✓ Template loaded: {template.layout_catalog.length} layouts available
        </p>
      </div>
      
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
          transition-colors duration-200
          ${isDragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
        `}
      >
        <input {...getInputProps()} />
        
        <svg
          className="mx-auto h-12 w-12 text-gray-400 mb-4"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
        >
          <path
            d="M9 12h6m-6 8h6m-6 8h6m10-16v6m-4-3h8m-8 8h8m-8 8h8M9 40h30a2 2 0 002-2V10a2 2 0 00-2-2H9a2 2 0 00-2 2v28a2 2 0 002 2z"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        
        {isDragActive ? (
          <p className="text-lg">Drop the source file here...</p>
        ) : (
          <>
            <p className="text-lg mb-2">
              Drag and drop your source presentation here
            </p>
            <p className="text-sm text-gray-500">
              Supports PPTX (high fidelity) and PDF (medium reliability)
            </p>
          </>
        )}
      </div>
      
      <div className="mt-4 text-sm text-gray-600">
        <p>• <strong>PPTX:</strong> High fidelity transformation</p>
        <p>• <strong>PDF:</strong> Medium/low reliability (structure inference)</p>
        <p>• Content will be mapped to template layouts automatically</p>
      </div>
    </div>
  );
}