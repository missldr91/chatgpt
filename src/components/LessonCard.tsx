import { Lesson } from '../data/sampleLessons';
import { Link } from 'react-router-dom';

interface Props {
  lesson: Lesson;
}

export default function LessonCard({ lesson }: Props) {
  return (
    <div className="border rounded shadow-sm overflow-hidden flex flex-col">
      <div className="h-32 bg-gray-100 flex items-center justify-center text-gray-400">Thumbnail</div>
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="font-semibold text-lg mb-2">{lesson.title}</h3>
        <p className="text-sm text-gray-500 mb-4">{lesson.slides} slides • {lesson.students} students</p>
        <div className="mt-auto flex justify-between text-sm">
          <Link to={`/lesson/${lesson.id}`} className="text-primary hover:underline">View</Link>
          <Link to={`/create?id=${lesson.id}`} className="text-accent hover:underline">Edit</Link>
        </div>
      </div>
    </div>
  );
}
