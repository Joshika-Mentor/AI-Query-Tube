import { useState } from "react";

export default function VideoCard({ video, rank }) {
  const [showTranscript, setShowTranscript] = useState(false);

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "12px",
        background: "#fff",
      }}
    >
      {/* Ranking + Score */}
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <span
          style={{
            background: "#1a73e8",
            color: "#fff",
            padding: "4px 8px",
            borderRadius: "4px",
            fontSize: "12px",
          }}
        >
          Rank #{rank}
        </span>

        <span
          style={{
            background: "#eee",
            padding: "4px 8px",
            borderRadius: "4px",
            fontSize: "12px",
          }}
        >
          Score: {video.score?.toFixed(3)}
        </span>
      </div>

      <h3 style={{ fontSize: "16px", margin: "10px 0" }}>
        {video.title}
      </h3>

      <iframe
        width="100%"
        height="200"
        src={`https://www.youtube.com/embed/${video.video_id}`}
        title={video.title}
        frameBorder="0"
        allowFullScreen
        style={{ borderRadius: "6px" }}
      />

      {/* Transcript toggle */}
      <button
        onClick={() => setShowTranscript(!showTranscript)}
        style={{
          marginTop: "10px",
          background: "none",
          border: "none",
          color: "#1a73e8",
          cursor: "pointer",
          padding: 0,
        }}
      >
        {showTranscript ? "Hide transcript" : "Show transcript"}
      </button>

      {showTranscript && (
        <p
          style={{
            marginTop: "8px",
            fontSize: "14px",
            color: "#444",
            maxHeight: "120px",
            overflow: "auto",
          }}
        >
          {video.transcript?.slice(0, 500)}...
        </p>
      )}
    </div>
  );
}
