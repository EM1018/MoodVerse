import { useState } from 'react'
import MoodBars from './MoodBars'

export default function ResultsView({ results, lyrics, songInfo, onReset }) {
  const [showLyrics, setShowLyrics] = useState(false)

  const confidencePct = Math.round(results.confidence * 100)

  return (
    <div className="flex flex-col gap-6">
      <hr className="border-neutral-700" />

      {/* Header row */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-2">
          <span className="text-xs tracking-widest text-neutral-400 uppercase">Detected mood</span>
          <h2
            className="text-5xl capitalize leading-tight"
            style={{ fontFamily: '"DM Serif Display", serif', color: '#534AB7' }}
          >
            {results.mood}
          </h2>
          <div className="flex items-center gap-1.5 w-fit px-3 py-1 rounded-full border border-neutral-600 text-sm text-neutral-200">
            <span className="text-green-400">✓</span>
            {confidencePct}% confidence
          </div>
        </div>

        {songInfo && (
          <div className="text-right">
            <p className="text-white font-medium">{songInfo.title}</p>
            <p className="text-neutral-400 text-sm">{songInfo.artist}</p>
          </div>
        )}
      </div>

      {/* Mood bars */}
      <div>
        <span className="text-xs tracking-widest text-neutral-400 uppercase block mb-4">
          Mood breakdown
        </span>
        <MoodBars scores={results.scores} topMood={results.mood} />
      </div>

      <hr className="border-neutral-700" />

      {/* Collapsible lyrics */}
      <div>
        <button
          onClick={() => setShowLyrics((v) => !v)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-neutral-600 text-sm text-neutral-200 hover:border-neutral-400 transition-colors"
        >
          <span>{showLyrics ? '∧' : '∨'}</span>
          {showLyrics ? 'Hide analyzed lyrics' : 'Show analyzed lyrics'}
        </button>

        {showLyrics && (
          <pre className="mt-4 text-neutral-400 text-sm whitespace-pre-wrap leading-relaxed">
            {lyrics}
          </pre>
        )}
      </div>

      {/* Try another */}
      <button
        onClick={onReset}
        className="flex items-center gap-2 px-4 py-2.5 w-fit rounded-full border border-neutral-600 text-sm text-neutral-200 hover:border-neutral-400 transition-colors"
      >
        <span>↺</span>
        Try another
      </button>
    </div>
  )
}
