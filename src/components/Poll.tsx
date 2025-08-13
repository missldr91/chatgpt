import { useState } from 'react';

interface Props {
  question: string;
  options: string[];
}

export default function Poll({ question, options }: Props) {
  const [votes, setVotes] = useState<number[]>(Array(options.length).fill(0));
  const [selected, setSelected] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);

  const total = votes.reduce((a, b) => a + b, 0);

  const handleVote = () => {
    if (selected === null) return;
    const newVotes = [...votes];
    newVotes[selected]++;
    setVotes(newVotes);
    setSubmitted(true);
  };

  return (
    <div className="border rounded p-4">
      <p className="font-semibold mb-2">{question}</p>
      {!submitted ? (
        <>
          <ul className="space-y-2 mb-4">
            {options.map((opt, idx) => (
              <li key={idx}>
                <label className="flex items-center space-x-2">
                  <input
                    type="radio"
                    name="poll"
                    value={idx}
                    checked={selected === idx}
                    onChange={() => setSelected(idx)}
                  />
                  <span>{opt}</span>
                </label>
              </li>
            ))}
          </ul>
          <button
            className="bg-primary text-white px-4 py-1 rounded"
            onClick={handleVote}
            disabled={selected === null}
          >
            Vote
          </button>
        </>
      ) : (
        <ul className="space-y-2">
          {options.map((opt, idx) => (
            <li key={idx} className="flex items-center">
              <span className="w-24">{opt}</span>
              <div className="flex-1 bg-gray-200 h-3 mx-2 rounded">
                <div
                  className="bg-accent h-3 rounded"
                  style={{ width: total ? `${(votes[idx] / total) * 100}%` : '0%' }}
                ></div>
              </div>
              <span>{votes[idx]}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
