const API_URL = "http://127.0.0.1:5600/search"; // Ensure full URL for local dev if needed

const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const loader = document.getElementById('loader');
const resultsGrid = document.getElementById('resultsGrid');

// Event Listeners
searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});

async function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        showToast("Please enter a search term");
        return;
    }

    // Reset UI
    resultsGrid.innerHTML = '';
    loader.classList.remove('hidden');
    resultsGrid.classList.add('hidden');

    try {
        const response = await fetch(`${API_URL}?query=${encodeURIComponent(query)}`);

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();

        loader.classList.add('hidden');
        resultsGrid.classList.remove('hidden');

        if (!data.results || data.results.length === 0) {
            showEmptyState();
            return;
        }

        renderResults(data.results);

    } catch (error) {
        console.error('Search error:', error);
        loader.classList.add('hidden');
        resultsGrid.classList.remove('hidden');
        showErrorState();
    }
}

function renderResults(videos) {
    // Add staggered animation delay
    videos.forEach((video, index) => {
        const scorePercent = Math.round(video.score * 100);
        const rawScore = video.score.toFixed(4); // Formatting the raw score
        const delay = index * 0.1; // 100ms stagger

        const card = document.createElement('div');
        card.className = 'video-card';
        card.style.animation = `fadeInUp 0.6s ease-out ${delay}s backwards`;

        card.innerHTML = `
            <div class="thumbnail-wrapper">
                <span class="match-badge">${scorePercent}% Match</span>
                <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
            </div>
            <div class="card-content">
                <h3 class="video-title" title="${video.title}">${video.title}</h3>
                <div style="margin-bottom: 8px; font-size: 0.85rem; color: var(--accent-primary); font-weight: 500;">
                    <i class="fa-solid fa-chart-line" style="margin-right: 5px;"></i>Score: ${rawScore}
                </div>
                <p class="video-desc">${video.description || "No description available for this video."}</p>
                <div class="card-footer">
                    <a href="https://www.youtube.com/watch?v=${video.video_id}" target="_blank" class="watch-btn">
                        <i class="fa-brands fa-youtube"></i> Watch Now
                    </a>
                </div>
            </div>
        `;

        resultsGrid.appendChild(card);
    });
}

function showEmptyState() {
    resultsGrid.innerHTML = `
        <div class="message-box">
            <i class="fa-regular fa-folder-open" style="font-size: 3rem; margin-bottom: 20px; color: var(--text-secondary);"></i>
            <h3>No matches found</h3>
            <p>Try adjusting your search terms or be less specific.</p>
        </div>
    `;
}

function showErrorState() {
    resultsGrid.innerHTML = `
        <div class="message-box">
            <i class="fa-solid fa-triangle-exclamation" style="font-size: 3rem; margin-bottom: 20px; color: var(--accent-primary);"></i>
            <h3>Connection Error</h3>
            <p>Is the backend server running?</p>
            <p style="font-size: 0.8rem; margin-top: 10px; opacity: 0.7;">python main.py</p>
        </div>
    `;
}

function showToast(message) {
    // Simple alert for now, could be enhanced to a custom toaster
    alert(message);
}
