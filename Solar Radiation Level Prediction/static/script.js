// Auto-fill the current time in the input field
document.addEventListener("DOMContentLoaded", () => {
  const timeButton = document.getElementById("set-current-time");
  const timeInput = document.getElementById("time");

  timeButton.addEventListener("click", () => {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");
    timeInput.value = `${hours}:${minutes}:${seconds}`;
  });
});
