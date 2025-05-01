window.addEventListener("DOMContentLoaded", async () => {
  const fileData = localStorage.getItem("uploadedFile");
  const manualText = localStorage.getItem("manualText");

  let summary = "";

  if (fileData) {
    // Process file upload as before
    const byteString = atob(fileData.split(',')[1]);
    const mimeString = fileData.split(',')[0].split(':')[1].split(';')[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([ab], { type: mimeString });

    const formData = new FormData();
    formData.append("file", blob, localStorage.getItem("fileName") || "document.pdf");

    try {
      const res = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      summary = data.summary || "Something went wrong!";
    } catch (error) {
      summary = "Error contacting the backend.";
    }

    localStorage.removeItem("uploadedFile");
    localStorage.removeItem("fileName");

  } else if (manualText) {
    // NEW: Send manual text to backend
    try {
      const res = await fetch("http://127.0.0.1:5000/summarize-text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: manualText })
      });

      const data = await res.json();
      summary = data.summary || "Something went wrong!";
    } catch (error) {
      summary = "Error contacting the backend.";
    }

    localStorage.removeItem("manualText");
  }

  localStorage.setItem("summary", summary);
  window.location.href = "summary.html";
});
