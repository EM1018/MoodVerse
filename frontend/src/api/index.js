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


export async function classifyMood(text) {
  await sleep(700);
  const res = await fetch(`${BASE_URL}/classify`, {
      method: 'POST',
      headers: { 'Content-Type': 'Application/JSON'},
      body: JSON.stringify({text})
  })
  if (!res.ok) return null; 
  return res.json();
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
