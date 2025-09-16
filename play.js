// play.js
function renderMedia(containerId) {
  const container = document.getElementById(containerId);
  const files = JSON.parse(localStorage.getItem("mediaFiles")) || [];

  if (!files.length) {
    container.innerHTML = "<p>No files uploaded yet.</p>";
    return;
  }

  files.forEach(file => {
    const div = document.createElement("div");
    div.className = "media-item";

    if (file.type.startsWith("video")) {
      div.innerHTML = `
        <video id="${file.name}" controls>
          <source src="${file.url}" type="${file.type}">
        </video><br>
        <button onclick="playMedia('${file.name}')">Play</button>
        <button onclick="pauseMedia('${file.name}')">Pause</button>
        <button onclick="stopMedia('${file.name}')">Stop</button>
      `;
    } else if (file.type.startsWith("audio")) {
      div.innerHTML = `
        <audio id="${file.name}" controls>
          <source src="${file.url}" type="${file.type}">
        </audio><br>
        <button onclick="playMedia('${file.name}')">Play</button>
        <button onclick="pauseMedia('${file.name}')">Pause</button>
        <button onclick="stopMedia('${file.name}')">Stop</button>
      `;
    } else if (file.type.startsWith("image")) {
      div.innerHTML = `<img src="${file.url}" alt="${file.name}" style="max-width:300px;">`;
    }

    container.appendChild(div);
  });
}

function playMedia(id) {
  document.getElementById(id).play();
}

function pauseMedia(id) {
  document.getElementById(id).pause();
}

function stopMedia(id) {
  const media = document.getElementById(id);
  media.pause();
  media.currentTime = 0;
}
