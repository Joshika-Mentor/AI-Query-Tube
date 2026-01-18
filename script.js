document.getElementById("btn").addEventListener("click", async () => {
  const query = document.getElementById("q").value || "dsa";
  const resultsDiv = document.getElementById("results");

  resultsDiv.innerHTML = "<p>Loading best lectures...</p>";

  try {
    const res = await fetch(
      "http://127.0.0.1:8000/search?query=" + encodeURIComponent(query)
    );
    const data = await res.json();

    resultsDiv.innerHTML = "";

   data.results.slice(0, 5).forEach(video => {
      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <img src="${video.thumbnail}" />
        <div class="card-content">
          <h3>${video.title}</h3>
          <p>${video.channel}</p>
          <p>👁 ${video.views} | 👍 ${video.likes}</p>
          <a href="https://www.youtube.com/watch?v=${video.video_id}" target="_blank">
            Watch Lecture →
          </a>
        </div>
      `;

      resultsDiv.appendChild(card);
    });

  } catch (err) {
    resultsDiv.innerHTML = "<p>❌ Backend not reachable</p>";
  }
});
