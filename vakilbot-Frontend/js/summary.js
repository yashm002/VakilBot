window.addEventListener("DOMContentLoaded", () => {
  const summary = localStorage.getItem("summary") || "No summary found.";
  document.getElementById("summary").innerText = summary;

  const downloadBtn = document.getElementById("downloadPdf");

  downloadBtn.addEventListener("click", () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({
      orientation: "p",
      unit: "mm",
      format: "a4",
    });

    const leftMargin = 15;
    const rightMargin = 15;
    const topMargin = 20;
    const lineHeight = 6;
    const pageHeight = doc.internal.pageSize.height;
    const pageWidth = doc.internal.pageSize.width;
    const textWidth = pageWidth - leftMargin - rightMargin;

    let y = topMargin;

    const lines = doc.splitTextToSize(summary, textWidth);

    doc.setFont("Helvetica", "normal");
    doc.setFontSize(12);

    for (let i = 0; i < lines.length; i++) {
      if (y + lineHeight > pageHeight - 20) {
        doc.addPage();
        y = topMargin;
      }
      doc.text(lines[i], leftMargin, y);
      y += lineHeight;
    }

    doc.save("VakilBot_Summary.pdf");
  });
});
