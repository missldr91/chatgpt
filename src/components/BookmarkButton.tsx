import { useState, useEffect } from 'react';

export default function BookmarkButton({ lessonId }: { lessonId: string }) {
  const key = `bookmark-${lessonId}`;
  const [bookmarked, setBookmarked] = useState(false);

  useEffect(() => {
    setBookmarked(localStorage.getItem(key) === '1');
  }, [key]);

  const toggle = () => {
    const next = !bookmarked;
    setBookmarked(next);
    localStorage.setItem(key, next ? '1' : '0');
  };

  return (
    <button
      className={`px-3 py-1 rounded border ${bookmarked ? 'bg-accent text-white' : 'bg-white text-gray-700'}`}
      onClick={toggle}
    >
      {bookmarked ? 'Bookmarked' : 'Bookmark'}
    </button>
  );
}
