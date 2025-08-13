interface Props {
  progress: number; // 0-100
}

export default function ProgressBar({ progress }: Props) {
  return (
    <div className="w-full bg-gray-200 rounded h-3">
      <div
        className="h-3 rounded bg-accent transition-all"
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );
}
