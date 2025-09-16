const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const loader = document.getElementById("loader");

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = role;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener("click", async () => {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage("user", "🧑: " + message);
  userInput.value = "";

  // Show loader
  loader.style.display = "block";

  try {
    const res = await fetch("http://127.0.0.1:5000/chat-news", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

    const data = await res.json();
    if (data.reply) {
      addMessage("assistant", "🤖: " + data.reply);
    } else {
      addMessage("assistant", "❌ Failed to get reply.");
    }
  } catch (err) {
    console.error("Fetch error:", err);
    addMessage("assistant", "❌ Error connecting to backend.");
  } finally {
    // Hide loader
    loader.style.display = "none";
  }
});
