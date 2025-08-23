'use client';

import React, { useState } from 'react';
import axios from 'axios';

export default function DebugPage() {
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);
  
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  const testUpload = async () => {
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    const file = fileInput?.files?.[0];
    
    if (!file) {
      setError('Please select a file');
      return;
    }
    
    setLoading(true);
    setError('');
    setResult(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      console.log('Uploading to:', `${API_URL}/templates/ingest`);
      
      const response = await axios.post(`${API_URL}/templates/ingest`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setResult(response.data);
      console.log('Success:', response.data);
    } catch (err: any) {
      console.error('Error:', err);
      setError(err.message + ' - ' + (err.response?.data?.detail || ''));
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Debug Upload Test</h1>
      
      <div className="mb-4">
        <p className="text-sm text-gray-600">API URL: {API_URL}</p>
      </div>
      
      <div className="mb-4">
        <input 
          type="file" 
          id="fileInput" 
          accept=".pptx"
          className="border p-2"
        />
      </div>
      
      <button
        onClick={testUpload}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
      >
        {loading ? 'Uploading...' : 'Test Upload'}
      </button>
      
      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          Error: {error}
        </div>
      )}
      
      {result && (
        <div className="mt-4 p-4 bg-green-100 rounded">
          <p className="text-green-700">Success!</p>
          <pre className="text-xs mt-2">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}