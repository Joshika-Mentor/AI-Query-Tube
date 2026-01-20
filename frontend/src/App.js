import { useState } from "react";
import SearchBar from "./components/SearchBar";
import VideoCard from "./components/VideoCard";
import LoadingSpinner from "./components/LoadingSpinner";
import LoadingSkeleton from "./components/LoadingSkeleton";
import { searchVideos } from "./api";

function App() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showSkeleton, setShowSkeleton] = useState(false);
  const [loadingText, setLoadingText] = useState("");

  async function handleSearch(query) {
    setLoading(true);
    setShowSkeleton(false);
    setVideos([]);
    setLoadingText("Searching videos...");

    // ⏱ Spinner → Skeleton after 1.5s
    const skeletonTimer = setTimeout(() => {
      setShowSkeleton(true);
      setLoadingText("Fetching transcripts...");
    }, 1500);

    try {
      const res = await searchVideos(query);
      setVideos(res);
    } catch (err) {
      console.error(err);
    } finally {
      clearTimeout(skeletonTimer);
      setLoading(false);
      setShowSkeleton(false);
    }
  }

  return (
    <div style={{ padding: 20, maxWidth: 1000, margin: "auto" }}>
      <h1>AI Query Tube</h1>

      <SearchBar onSearch={handleSearch} loading={loading} />

      {loading && !showSkeleton && (
        <LoadingSpinner text={loadingText} />
      )}

      {loading && showSkeleton && <LoadingSkeleton />}

      {!loading && videos.length === 0 && (
        <p style={{ marginTop: 20, color: "#777" }}>
          No results yet
        </p>
      )}

      {!loading && videos.length > 0 && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: 20,
            marginTop: 30,
            animation: "fadeIn 0.5s ease-in",
          }}
        >
          {videos.map((v, index) => (
            <VideoCard
              key={v.video_id}
              video={v}
              rank={index + 1}
            />
          ))}

          <style>
            {`
              @keyframes fadeIn {
                from { opacity: 0; transform: translateY(5px); }
                to { opacity: 1; transform: translateY(0); }
              }
            `}
          </style>
        </div>
      )}
    </div>
  );
}

export default App;
