import { Routes, Route, Link } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import TutorDashboard from './pages/TutorDashboard';
import LessonCreator from './pages/LessonCreator';
import LessonViewer from './pages/LessonViewer';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/dashboard" element={<TutorDashboard />} />
      <Route path="/create" element={<LessonCreator />} />
      <Route path="/lesson/:id" element={<LessonViewer />} />
      <Route path="*" element={<div className="p-8">Page Not Found. <Link to="/" className="text-primary">Go home</Link></div>} />
    </Routes>
  );
}
