import { useState } from 'react';
import Quiz from '../components/Quiz';
import Poll from '../components/Poll';

export default function LessonCreator() {
  const [step, setStep] = useState<'upload' | 'processing' | 'preview'>('upload');
  const [progress, setProgress] = useState(0);

  const startProcessing = (files: FileList | null) => {
    if (!files || !files[0]) return;
    setStep('processing');
    setProgress(0);
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 100) {
          clearInterval(interval);
          setStep('preview');
          return 100;
        }
        return p + 10;
      });
    }, 200);
  };

  if (step === 'upload') {
    return (
      <div className="p-6">
        <h2 className="text-2xl font-heading font-bold mb-4">Create Lesson</h2>
        <div className="border-dashed border-2 border-gray-300 p-8 text-center rounded" onDragOver={e => e.preventDefault()} onDrop={e => {e.preventDefault(); startProcessing(e.dataTransfer.files);}}>
          <p className="mb-4">Upload your PPT/PDF to start.</p>
          <input type="file" accept=".ppt,.pptx,.pdf" onChange={e => startProcessing(e.target.files)} className="block mx-auto" />
        </div>
      </div>
    );
  }

  if (step === 'processing') {
    return (
      <div className="p-6 text-center">
        <h2 className="text-2xl font-heading font-bold mb-4">Processing File</h2>
        <p className="mb-4">This may take a moment...</p>
        <div className="w-64 mx-auto bg-gray-200 h-3 rounded">
          <div className="h-3 bg-primary rounded" style={{ width: `${progress}%` }}></div>
        </div>
        <p className="mt-2">{progress}%</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-heading font-bold">Preview & Customize</h2>
      <div className="border rounded p-4">
        <p className="mb-2 font-semibold">Slide 1</p>
        <img src="https://via.placeholder.com/600x300" alt="Slide preview" className="mb-4 w-full" />
        <Quiz
          question={{
            question: 'What is Machine Learning?',
            options: ['A type of hardware', 'A method for computers to learn from data', 'A programming language'],
            answer: 1,
            explanation: 'Machine learning enables computers to learn patterns from data.',
          }}
        />
      </div>
      <div className="border rounded p-4">
        <p className="mb-2 font-semibold">Slide 2</p>
        <img src="https://via.placeholder.com/600x300" alt="Slide preview" className="mb-4 w-full" />
        <Poll question="Which type of algorithm is best for classification?" options={["Decision Trees", "K-Means", "Gradient Descent"]} />
      </div>
      <button className="bg-accent text-white px-6 py-2 rounded">Publish Lesson</button>
    </div>
  );
}
