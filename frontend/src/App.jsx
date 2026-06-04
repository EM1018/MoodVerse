import { useState } from 'react'
import TabInput from './components/TabInput'
import ResultsView from './components/ResultsView'
import { fetchLyrics, classifyMood } from './api/index'

export default function App() {
  const [activeTab, setActiveTab] = useState('text')
  const [results, setResults] = useState(null)
  const [lyrics, setLyrics] = useState('')
  const [songInfo, setSongInfo] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingMsg, setLoadingMsg] = useState('')
  const [inputKey, setInputKey] = useState(0)

  async function handleClassify({ mode, text, title, artist }) {
    setLoading(true)
    setResults(null)

    try {
      let textToClassify = ''

      if (mode === 'song') {
        setLoadingMsg('Fetching lyrics… via Genius API')
        const data = await fetchLyrics(title, artist)
        textToClassify = data.text
        setLyrics(data.text)
        setSongInfo({ title: data.title, artist: data.artist })
        setLoadingMsg('Classifying mood… running model')
      } else {
        setLoadingMsg('Classifying mood… running model')
        textToClassify = text
        setLyrics(text)
        setSongInfo(null)
      }

      const result = await classifyMood(textToClassify)
      setResults(result)
    } finally {
      setLoading(false)
      setLoadingMsg('')
    }
  }

  function handleReset() {
    setResults(null)
    setLyrics('')
    setSongInfo(null)
    setInputKey((k) => k + 1)
  }

  function handleTabChange(tab) {
    setActiveTab(tab)
    setResults(null)
    setLyrics('')
    setSongInfo(null)
  }

  return (
    <div
      className="min-h-screen text-white px-6 py-10"
      style={{ backgroundColor: '#1a1a1f', fontFamily: '"DM Sans", sans-serif' }}
    >
      <div className="max-w-2xl mx-auto flex flex-col gap-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            <span style={{ fontFamily: '"DM Sans", sans-serif' }}>mood</span>
            <span style={{ fontFamily: '"DM Serif Display", serif', color: '#7F77DD', fontStyle: 'italic' }}>
              verse
            </span>
          </h1>
          <p className="text-neutral-400 text-sm mt-1">
            Classify the emotional tone of lyrics, quotes, or any text.
          </p>
        </div>

        {/* Input */}
        <TabInput
          key={inputKey}
          activeTab={activeTab}
          onTabChange={handleTabChange}
          onClassify={handleClassify}
          loading={loading}
          loadingMsg={loadingMsg}
        />

        {/* Results */}
        {results && (
          <ResultsView
            results={results}
            lyrics={lyrics}
            songInfo={songInfo}
            onReset={handleReset}
          />
        )}
      </div>
    </div>
  )
}
