import { useState } from "react";

export default function SearchBar({ onSearch, loading = false }) {
  const [query, setQuery] = useState("");

  function triggerSearch() {
    if (query.trim()) {
      onSearch(query);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        gap: "10px",
        marginTop: "15px",
        marginBottom: "20px",
        alignItems: "center",
      }}
    >
      <input
        type="text"
        value={query}
        placeholder={
          loading ? "Searching videos..." : "Search YouTube semantically..."
        }
        disabled={loading}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") triggerSearch();
        }}
        style={{
          flex: 1,
          padding: "12px",
          fontSize: "16px",
          borderRadius: "6px",
          border: "1px solid #ccc",
          outline: "none",
        }}
      />

      <button
        onClick={triggerSearch}
        disabled={loading}
        style={{
          padding: "12px 18px",
          fontSize: "16px",
          borderRadius: "6px",
          border: "none",
          backgroundColor: "#1a73e8",
          color: "white",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        🔍
      </button>
    </div>
  );
}
