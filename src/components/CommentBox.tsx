import { useState } from 'react';

export default function CommentBox() {
  const [comments, setComments] = useState<string[]>([]);
  const [text, setText] = useState('');

  const submit = () => {
    if (!text.trim()) return;
    setComments([...comments, text.trim()]);
    setText('');
  };

  return (
    <div className="mt-4">
      <textarea
        className="w-full border rounded p-2 mb-2"
        rows={3}
        placeholder="Leave feedback..."
        value={text}
        onChange={e => setText(e.target.value)}
      ></textarea>
      <button
        className="bg-primary text-white px-4 py-1 rounded"
        onClick={submit}
      >
        Comment
      </button>
      <ul className="mt-4 space-y-2">
        {comments.map((c, idx) => (
          <li key={idx} className="border rounded p-2 bg-gray-50">{c}</li>
        ))}
      </ul>
    </div>
  );
}
