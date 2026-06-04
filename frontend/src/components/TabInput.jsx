import { useState } from 'react'

export default function TabInput({ activeTab, onTabChange, onClassify, loading, loadingMsg, songError, onClearError }) {
  const [text, setText] = useState('')
  const [title, setTitle] = useState('')
  const [artist, setArtist] = useState('')

  function handleSubmit() {
    if (activeTab === 'text') {
      onClassify({ mode: 'text', text })
    } else {
      onClassify({ mode: 'song', title, artist })
    }
  }

  const canSubmit = !loading && (activeTab === 'text' ? text.trim() : title.trim())

  return (
    <div className="flex flex-col gap-5">
      {/* Tabs */}
      <div className="flex gap-0 w-fit border border-neutral-600 rounded-full overflow-hidden">
        {['text', 'song'].map((tab) => {
          const label = tab === 'text' ? 'Paste text' : 'Look up a song'
          const active = activeTab === tab
          return (
            <button
              key={tab}
              onClick={() => onTabChange(tab)}
              className={`px-5 py-2 text-sm font-medium transition-colors ${
                active
                  ? 'bg-white text-black'
                  : 'bg-transparent text-neutral-300 hover:text-white'
              }`}
            >
              {label}
            </button>
          )
        })}
      </div>

      {/* Input area */}
      {activeTab === 'text' ? (
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste lyrics or a quote here..."
          rows={7}
          className="w-full bg-neutral-800 text-white placeholder-neutral-500 rounded-lg p-4 text-sm resize-y border border-neutral-700 focus:outline-none focus:border-neutral-500"
        />
      ) : (
        <div className="flex flex-col gap-2">
          <div className="flex gap-3">
            <input
              value={title}
              onChange={(e) => { setTitle(e.target.value); onClearError?.() }}
              placeholder="Song title"
              className="flex-[3] bg-neutral-800 text-white placeholder-neutral-500 rounded-lg px-4 py-3 text-sm border border-neutral-700 focus:outline-none focus:border-neutral-500"
            />
            <input
              value={artist}
              onChange={(e) => { setArtist(e.target.value); onClearError?.() }}
              placeholder="Artist (optional)"
              className="flex-[1] bg-neutral-800 text-white placeholder-neutral-500 rounded-lg px-4 py-3 text-sm border border-neutral-700 focus:outline-none focus:border-neutral-500"
            />
          </div>
          {songError
            ? <p className="text-red-400 text-xs">{songError}</p>
            : <p className="text-neutral-500 text-xs">Adding an artist helps find the right song.</p>
          }
        </div>
      )}

      {/* Button / loading */}
      {loading ? (
        <p className="text-neutral-400 text-sm">{loadingMsg}</p>
      ) : (
        <button
          onClick={handleSubmit}
          disabled={!canSubmit}
          className="flex items-center gap-2 px-5 py-3 w-fit rounded-full text-sm font-medium text-white transition-opacity disabled:opacity-40"
          style={{ backgroundColor: '#7F77DD' }}
        >
          <span>✦</span>
          Classify mood
        </button>
      )}
    </div>
  )
}
