const BASE_URL = 'http://localhost:8000';

// TODO: replace mock with → POST ${BASE_URL}/lyrics
export async function fetchLyrics(_title, _artist) {
  await sleep(900);
  return {
    title: "Flightless Bird, American Mouth",
    artist: "Iron & Wine",
    text: "I was a quick wet boy\nDiving too deep for coins\nAll of your street light eyes\nWide on my plastic toys..."
  };
}

// TODO: replace mock with → POST ${BASE_URL}/classify
export async function classifyMood(_text) {
  await sleep(700);
  return {
    mood: "melancholic",
    confidence: 0.87,
    scores: {
      melancholic: 0.87,
      sad: 0.61,
      nostalgic: 0.44,
      romantic: 0.19,
      angry: 0.08,
      happy: 0.03
    }
  };
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
