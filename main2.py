import streamlit as st
import streamlit.components.v1 as components

html_content = """

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Turbo - Learn Smarter</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: "Segoe UI", sans-serif;
      background: #111;
      color: #fff;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    #app {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      text-align: center;
      flex-direction: column;
      padding: 40px;
      overflow-y: auto;
    }
    h1 {
      font-size: 3rem;
      margin-bottom: 20px;
      letter-spacing: 2px;
    }
    input {
      background: none;
      border: none;
      border-bottom: 2px solid #fff;
      color: #fff;
      font-size: 1.5rem;
      padding: 10px;
      width: 60%;
      text-align: center;
      outline: none;
    }
    button {
      margin-top: 20px;
      padding: 12px 24px;
      font-size: 1.2rem;
      background: #fff;
      color: #000;
      border: none;
      border-radius: 30px;
      cursor: pointer;
      transition: all 0.3s;
    }
    button:hover { background: #ddd; }
    .video-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 30px;
      margin-top: 40px;
      width: 100%;
    }
    iframe {
      width: 100%;
      height: 250px;
      border: none;
      border-radius: 12px;
    }
    ul {
      text-align: left;
      margin-top: 8px;
      color: #ccc;
      font-size: 0.9rem;
      padding-left: 20px;
    }
    .fade { animation: fadeIn 1s ease-in; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  </style>
</head>
<body>
  <div id="app" class="fade">
    <h1>Turbo</h1>
    <p style="font-size:1.5rem;margin-bottom:20px;">What do you want to learn today?</p>
    <input id="topic" placeholder="Type a subject..." />
    <button onclick="startLearning()">Learn</button>
  </div>

  <script>
    const API_KEY = "AIzaSyBxlRvIEPCu5P88zU_QVHGwKqZDWVy4F08";

    function parseDuration(duration) {
      const match = duration.match(/PT(?:(\d+)M)?(?:(\d+)S)?/);
      const minutes = match && match[1] ? parseInt(match[1]) : 0;
      const seconds = match && match[2] ? parseInt(match[2]) : 0;
      return minutes * 60 + seconds;
    }

    async function startLearning() {
      const topic = document.getElementById("topic").value.trim().toLowerCase();
      if (!topic) return;

      try {
        // Search videos
        const searchUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=15&q=${encodeURIComponent(topic)}&key=${API_KEY}`;
        const searchRes = await fetch(searchUrl);
        const searchData = await searchRes.json();
        if (!searchData.items || searchData.items.length === 0) {
          app.innerHTML = `<h1>Turbo</h1><p>No videos found for "${topic}".</p><button onclick="location.reload()">Try Again</button>`;
          return;
        }

        const videoIds = searchData.items.map(item => item.id.videoId).join(",");
        const detailsUrl = `https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id=${videoIds}&key=${API_KEY}`;
        const detailsRes = await fetch(detailsUrl);
        const detailsData = await detailsRes.json();

        // Filter out Shorts (≤ 3 minutes)
        const nonShorts = detailsData.items.filter(video => parseDuration(video.contentDetails.duration) > 180);
        const top3 = nonShorts.slice(0, 3);

        if (top3.length === 0) {
          app.innerHTML = `<h1>Turbo</h1><p>Only Shorts found for "${topic}".</p><button onclick="location.reload()">Try Again</button>`;
          return;
        }

        // Build HTML
        let html = `<h1>Turbo</h1><p style="font-size:1.5rem;">Top videos for <b>${topic}</b> (No Shorts):</p>`;
        html += `<div class="video-grid">`;
        top3.forEach(video => {
          const videoId = video.id;
          const title = video.snippet.title.replace(/`/g, "'");

          // Extract first 2–3 bullets from description
          let bullets = (video.snippet.description || "")
                          .split(/[.?!]\s+/)
                          .filter(b => b.trim() !== "")
                          .slice(0, 3);
          let bulletsHtml = "<ul>" + bullets.map(b => `<li>${b}</li>`).join("") + "</ul>";

          html += `
            <div>
              <p><b>${title}</b></p>
              <iframe src="https://www.youtube.com/embed/${videoId}" allowfullscreen></iframe>
              ${bulletsHtml}
            </div>
          `;
        });
        html += `</div>`;
        html += `<button style="margin-top:30px;" onclick="location.reload()">Learn Something Else</button>`;

        app.innerHTML = html;

      } catch (err) {
        console.error(err);
        app.innerHTML = `<h1>Turbo</h1><p>Something went wrong fetching videos.</p><button onclick="location.reload()">Try Again</button>`;
      }
    }
  </script>
</body>
</html>

"""

# Embed the HTML content using st.components.v1.html
components.html(html_content, height=400)
