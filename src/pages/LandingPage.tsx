import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="p-6 flex justify-between items-center">
        <h1 className="text-2xl font-heading font-bold text-primary">SlideFlow</h1>
        <nav className="space-x-4">
          <Link to="/dashboard" className="text-sm text-gray-600 hover:text-primary">Dashboard</Link>
        </nav>
      </header>
      <main className="flex-1 flex flex-col items-center justify-center px-4 text-center">
        <h2 className="font-heading text-4xl md:text-5xl font-bold mb-4">Transform Your Slides Into Interactive Experiences</h2>
        <p className="text-lg text-gray-600 mb-8 max-w-2xl">SlideFlow converts boring decks into engaging lessons with quizzes, polls and analytics. Tutors upload. Students interact. Everyone learns.</p>
        <div className="space-x-4">
          <Link to="/create" className="bg-primary text-white px-6 py-3 rounded shadow">Start Creating</Link>
          <Link to="/lesson/ml-intro" className="bg-accent text-white px-6 py-3 rounded shadow">View Demo</Link>
        </div>
        <section className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-4xl">
          <div className="p-6 border rounded shadow-sm">
            <h3 className="font-semibold mb-2">Easy Upload</h3>
            <p className="text-sm text-gray-600">Drag and drop your PPT or PDF to get started.</p>
          </div>
          <div className="p-6 border rounded shadow-sm">
            <h3 className="font-semibold mb-2">Smart Interactions</h3>
            <p className="text-sm text-gray-600">Quizzes, polls and comments keep students engaged.</p>
          </div>
          <div className="p-6 border rounded shadow-sm">
            <h3 className="font-semibold mb-2">Track Progress</h3>
            <p className="text-sm text-gray-600">See completion rates and time spent per slide.</p>
          </div>
        </section>
      </main>
      <footer className="p-6 text-center text-sm text-gray-500">© 2024 SlideFlow</footer>
    </div>
  );
}
