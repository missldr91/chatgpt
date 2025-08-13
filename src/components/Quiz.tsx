import { useState } from 'react';

interface Question {
  question: string;
  options: string[];
  answer: number;
  explanation?: string;
}

interface Props {
  question: Question;
}

export default function Quiz({ question }: Props) {
  const [selected, setSelected] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => setSubmitted(true);

  return (
    <div className="border rounded p-4">
      <p className="font-semibold mb-2">{question.question}</p>
      <ul className="space-y-2 mb-4">
        {question.options.map((opt, idx) => (
          <li key={idx}>
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                name="quiz"
                value={idx}
                checked={selected === idx}
                onChange={() => setSelected(idx)}
                disabled={submitted}
              />
              <span>{opt}</span>
            </label>
          </li>
        ))}
      </ul>
      {!submitted ? (
        <button
          className="bg-primary text-white px-4 py-1 rounded"
          onClick={handleSubmit}
          disabled={selected === null}
        >
          Submit
        </button>
      ) : (
        <div className="mt-2">
          {selected === question.answer ? (
            <p className="text-accent font-medium">Correct!</p>
          ) : (
            <p className="text-red-500 font-medium">Incorrect.</p>
          )}
          {question.explanation && (
            <p className="text-sm text-gray-600 mt-1">{question.explanation}</p>
          )}
        </div>
      )}
    </div>
  );
}
