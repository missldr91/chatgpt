'use client';

import React from 'react';
import { useStore } from '@/lib/store';
import { TemplateUpload } from '@/components/TemplateUpload';
import { SourceUpload } from '@/components/SourceUpload';
import { PlanPreview } from '@/components/PlanPreview';

export default function Home() {
  const { currentStep, template, source, plan, isLoading, error, reset } = useStore();
  
  return (
    <div className="py-8">
      {/* Progress Bar */}
      <div className="max-w-4xl mx-auto px-4 mb-8">
        <div className="flex items-center justify-between">
          {['Template', 'Source', 'Review', 'Export'].map((step, idx) => {
            const stepKey = step.toLowerCase() as 'template' | 'source' | 'plan' | 'export';
            const steps = ['template', 'source', 'plan', 'export'];
            const currentIndex = steps.indexOf(currentStep);
            const isActive = idx <= currentIndex;
            
            return (
              <div key={step} className="flex items-center">
                <div className={`
                  w-10 h-10 rounded-full flex items-center justify-center font-semibold
                  ${isActive ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'}
                `}>
                  {idx + 1}
                </div>
                <span className={`ml-2 ${isActive ? 'text-gray-900' : 'text-gray-500'}`}>
                  {step}
                </span>
                {idx < 3 && (
                  <div className={`w-16 h-1 ml-4 ${isActive ? 'bg-blue-600' : 'bg-gray-300'}`} />
                )}
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Error Display */}
      {error && (
        <div className="max-w-4xl mx-auto px-4 mb-6">
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800">❌ {error}</p>
          </div>
        </div>
      )}
      
      {/* Loading Overlay */}
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Processing...</p>
          </div>
        </div>
      )}
      
      {/* Main Content */}
      <div className="relative">
        {/* Template Upload */}
        {currentStep === 'template' && !template && (
          <TemplateUpload />
        )}
        
        {/* Source Upload */}
        {(currentStep === 'source' || (currentStep === 'template' && template)) && !source && (
          <SourceUpload />
        )}
        
        {/* Plan Preview */}
        {(currentStep === 'plan' || currentStep === 'export') && plan && (
          <PlanPreview />
        )}
      </div>
      
      {/* Reset Button */}
      {(template || source || plan) && (
        <div className="fixed bottom-6 right-6">
          <button
            onClick={reset}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 shadow-lg"
          >
            Start Over
          </button>
        </div>
      )}
    </div>
  );
}