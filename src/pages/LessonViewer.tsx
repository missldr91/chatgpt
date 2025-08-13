import { useParams } from 'react-router-dom';
import { useState } from 'react';
import Quiz from '../components/Quiz';
import Poll from '../components/Poll';
import CommentBox from '../components/CommentBox';
import ProgressBar from '../components/ProgressBar';
import BookmarkButton from '../components/BookmarkButton';

export default function LessonViewer() {
  const { id } = useParams();
  const slides = [
    {
      title: 'What is Machine Learning?',
      img: 'https://via.placeholder.com/600x300',
      quiz: {
        question: 'What is Machine Learning?',
        options: ['Rule-based programming', 'Learning from data', 'Manual coding of logic'],
        answer: 1,
        explanation: 'Machine Learning lets computers learn patterns from data.',
      },
    },
    {
      title: 'Algorithm Types',
      img: 'https://via.placeholder.com/600x300',
      poll: {
        question: 'Which type of algorithm is best for classification?',
        options: ['Decision Trees', 'K-Means', 'Gradient Descent'],
      },
    },
  ];

  const [index, setIndex] = useState(0);
  const progress = ((index + 1) / slides.length) * 100;

  const next = () => setIndex(i => Math.min(i + 1, slides.length - 1));
  const prev = () => setIndex(i => Math.max(i - 1, 0));

  const slide = slides[index];

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <header className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-heading font-bold">Lesson: {id}</h2>
        {id && <BookmarkButton lessonId={id} />}
      </header>
      <ProgressBar progress={progress} />
      <div className="mt-6">
        <h3 className="font-semibold mb-2">{slide.title}</h3>
        <img src={slide.img} alt="slide" className="mb-4 w-full" />
        {slide.quiz && <Quiz question={slide.quiz} />}
        {slide.poll && <Poll question={slide.poll.question} options={slide.poll.options} />}
        <CommentBox />
      </div>
      <div className="flex justify-between mt-6">
        <button className="px-4 py-2 bg-gray-200 rounded" onClick={prev} disabled={index === 0}>
          Previous
        </button>
        <button className="px-4 py-2 bg-primary text-white rounded" onClick={next} disabled={index === slides.length - 1}>
          Next
        </button>
      </div>
    </div>
  );
}
