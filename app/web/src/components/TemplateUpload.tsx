'use client';

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useStore } from '@/lib/store';
import { uploadTemplate } from '@/lib/api';

export function TemplateUpload() {
  const { setTemplate, setLoading, setError } = useStore();
  
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;
    
    if (!file.name.endsWith('.pptx')) {
      setError('Please upload a PPTX file');
      return;
    }
    
    console.log('Uploading file:', file.name, 'Size:', file.size);
    
    setLoading(true);
    try {
      const template = await uploadTemplate(file);
      console.log('Upload successful:', template);
      setTemplate(template);
    } catch (error: any) {
      console.error('Upload error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to upload template';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [setTemplate, setLoading, setError]);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx']
    },
    maxFiles: 1,
  });
  
  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Step 1: Upload Brand Template</h2>
      
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
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        
        {isDragActive ? (
          <p className="text-lg">Drop the template here...</p>
        ) : (
          <>
            <p className="text-lg mb-2">
              Drag and drop your brand template PPTX here
            </p>
            <p className="text-sm text-gray-500">
              or click to select file
            </p>
          </>
        )}
      </div>
      
      <div className="mt-4 text-sm text-gray-600">
        <p>• Upload your branded PowerPoint template</p>
        <p>• The template should contain your brand colors, fonts, and layouts</p>
        <p>• Maximum file size: 50MB</p>
      </div>
    </div>
  );
}