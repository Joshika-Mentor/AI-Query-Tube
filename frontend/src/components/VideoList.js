import VideoCard from "./VideoCard";

export default function VideoList({ videos }) {
  return (
    <div style={{ marginTop: 20 }}>
      {videos.map((v) => (
        <VideoCard key={v.video_id} video={v} />
      ))}
    </div>
  );
}
