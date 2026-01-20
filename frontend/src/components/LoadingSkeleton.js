export default function LoadingSkeleton() {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(2, 1fr)",
        gap: 20,
        marginTop: 30,
      }}
    >
      {Array.from({ length: 4 }).map((_, i) => (
        <div
          key={i}
          style={{
            background: "#eee",
            borderRadius: 8,
            padding: 10,
            animation: "pulse 1.5s infinite",
          }}
        >
          <div
            style={{
              height: 180,
              background: "#ddd",
              borderRadius: 6,
              marginBottom: 10,
            }}
          />
          <div style={{ height: 16, background: "#ddd", width: "80%" }} />
        </div>
      ))}

      <style>
        {`
          @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
          }
        `}
      </style>
    </div>
  );
}
