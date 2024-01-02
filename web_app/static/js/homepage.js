function validateUrl() {
  const urlInput = document.getElementById("url");
  const formatSelect = document.getElementById("format");
  const errorMessage = document.getElementById("error-message");

  const url = urlInput.value.trim();

  const youtubeRegex =
    /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|v\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;

  if (!url.match(youtubeRegex)) {
    errorMessage.innerHTML = "Please enter a valid YouTube URL.";
    return false;
  }

  errorMessage.innerHTML = "";
  return true;
}
