import { useState } from 'react';
import StatsCard from '../components/StatsCard';
import LessonCard from '../components/LessonCard';
import { lessons } from '../data/sampleLessons';

export default function TutorDashboard() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleUpload = (files: FileList | null) => {
    if (!files || !files[0]) return;
    setUploading(true);
    setProgress(0);
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 100) {
          clearInterval(interval);
          setUploading(false);
          return 100;
        }
        return p + 10;
      });
    }, 200);
  };

  return (
    <div className="p-6 space-y-6">
      <header className="flex justify-between items-center">
        <h2 className="text-2xl font-heading font-bold">Dashboard</h2>
        <div className="flex items-center space-x-4">
          <div className="text-sm">Tutor</div>
        </div>
      </header>
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard label="Total Lessons" value={lessons.length} />
        <StatsCard label="Total Students" value={lessons.reduce((a, l) => a + l.students, 0)} />
        <StatsCard label="Avg Completion" value="86%" />
        <StatsCard label="Avg Time Spent" value="12m" />
      </section>
      <section className="border-dashed border-2 border-gray-300 p-8 text-center rounded" onDragOver={e => e.preventDefault()} onDrop={e => {e.preventDefault(); handleUpload(e.dataTransfer.files);}}>
        <p className="mb-4">Drag & drop PPT/PDF files here or click to upload.</p>
        <input type="file" accept=".ppt,.pptx,.pdf" onChange={e => handleUpload(e.target.files)} className="block mx-auto" />
        {uploading && <div className="mt-4">Processing... {progress}%</div>}
      </section>
      <section>
        <h3 className="font-semibold mb-4">Your Lessons</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {lessons.map(l => (
            <LessonCard key={l.id} lesson={l} />
          ))}
        </div>
      </section>
    </div>
  );
}
