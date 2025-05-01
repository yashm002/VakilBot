function goToLoading() {
  const text = document.getElementById("text").value;
  if (text.trim()) {
    localStorage.setItem("manualText", text);
    window.location.href = "loading.html";
  } else {
    alert("Please upload a file or paste text!");
  }
}