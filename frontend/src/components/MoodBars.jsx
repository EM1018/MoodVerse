import { useEffect, useState } from 'react'

export default function MoodBars({ scores, topMood }) {
  const [animated, setAnimated] = useState(false)

  useEffect(() => {
    const id = requestAnimationFrame(() => setAnimated(true))
    return () => cancelAnimationFrame(id)
  }, [])

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1])

  return (
    <div className="flex flex-col gap-3">
      {sorted.map(([mood, score]) => {
        const isTop = mood === topMood
        const pct = Math.round(score * 100)
        return (
          <div key={mood} className="flex items-center gap-3">
            <span
              className={`w-24 text-sm text-right capitalize ${isTop ? 'text-white font-semibold' : 'text-neutral-400'}`}
            >
              {mood}
            </span>
            <div className="flex-1 h-2 bg-neutral-700 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700 ease-out"
                style={{
                  width: animated ? `${pct}%` : '0%',
                  backgroundColor: isTop ? '#7F77DD' : '#4B4A6A',
                }}
              />
            </div>
            <span
              className={`w-10 text-sm text-right ${isTop ? 'text-[#7F77DD] font-semibold' : 'text-neutral-400'}`}
            >
              {pct}%
            </span>
          </div>
        )
      })}
    </div>
  )
}
