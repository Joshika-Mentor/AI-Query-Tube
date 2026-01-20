export async function searchVideos(query) {
  const res = await fetch(
    `http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`
  );

  if (!res.ok) {
    throw new Error("Backend error");
  }

  const data = await res.json();

  // ✅ FIX: extract results
  return data.results || [];
}
