const BASE_URL = 'http://localhost:8000';

export async function fetchLyrics(title, artist) {
  const res = await fetch(`${BASE_URL}/lyrics`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, artist }),
  });
  if (!res.ok) return null;
  return res.json();
}

// TODO: replace mock with → POST ${BASE_URL}/classify
export async function classifyMood(text) {
  await sleep(700);
  /*return {
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
  };*/ 
  const res = await fetch(`${BASE_URL}/classify`, {
      method: 'POST',
      headers: { 'Content-Type': 'Application/JSON'},
      body: JSON.stringify({text})
  })
  if (!res.ok) return null; 
  return res.json();
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
