// upload.js
function saveFiles(inputId, messageId) {
  const input = document.getElementById(inputId);
  const message = document.getElementById(messageId);

  if (!input || !input.files.length) {
    message.textContent = "❌ No files selected!";
    return;
  }

  let storedFiles = JSON.parse(localStorage.getItem("mediaFiles")) || [];

  for (let file of input.files) {
    const fileURL = URL.createObjectURL(file);
    storedFiles.push({ name: file.name, type: file.type, url: fileURL });
  }

  localStorage.setItem("mediaFiles", JSON.stringify(storedFiles));
  message.textContent = "✅ Files saved successfully!";
}
