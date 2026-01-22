const API_URL = "http://127.0.0.1:8000/search"; // FastAPI endpoint

// 🔹 Enable ENTER key to trigger search
document.addEventListener("DOMContentLoaded", () => {
    const queryInput = document.getElementById("query");

    queryInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            searchVideos();
        }
    });
});

async function searchVideos() {
    const queryInput = document.getElementById("query");
    const resultsDiv = document.getElementById("results");

    const query = queryInput.value.trim();

    if (!query) {
        alert("Please enter a search query");
        return;
    }

    // Show loading text
    resultsDiv.innerHTML = `
        <p style="text-align:center; color:#ccc;">
            Searching YouTube for "${query}"...
        </p>
    `;

    try {
        const response = await fetch(
            `${API_URL}?query=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error("Failed to fetch results");
        }

        const data = await response.json();

        // Backend returns array directly
        if (!Array.isArray(data) || data.length === 0) {
            resultsDiv.innerHTML = `
                <p style="text-align:center; color:#ffaaaa;">
                    No results found
                </p>
            `;
            return;
        }

        displayResults(data);

    } catch (error) {
        console.error(error);
        resultsDiv.innerHTML = `
            <p style="text-align:center; color:red;">
                Error connecting to backend
            </p>
        `;
    }
}

function displayResults(videos) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    videos.forEach(video => {
        const card = document.createElement("div");
        card.className = "video-card";

        // If backend sends video_id, auto-generate thumbnail
        const thumbnail =
            video.thumbnail ||
            `https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`;

        card.innerHTML = `
            <img src="${thumbnail}" class="video-thumbnail" alt="thumbnail">
            <div class="video-info">
                <div class="video-title">${video.title}</div>
                <div class="video-channel">
                    ${video.channel || "YouTube Channel"}
                </div>
                <div class="video-meta">
                    ${video.views || ""}
                </div>
            </div>
        `;

        // Click card → open YouTube
        card.onclick = () => {
            window.open(
                video.url || `https://www.youtube.com/watch?v=${video.video_id}`,
                "_blank"
            );
        };

        resultsDiv.appendChild(card);
    });
}
