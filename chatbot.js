$(document).ready(function () {
  const chatbotToggle = $("#chatbotToggle");
  const chatbotContainer = $("#chatbotContainer");
  const chatbotClose = $("#chatbotClose");
  const chatMessages = $("#chatMessages");
  const chatInput = $("#chatInput");
  const sendMessage = $("#sendMessage");

  // 🟢 Open chatbot
  chatbotToggle.on("click", () => chatbotContainer.removeClass("hidden"));

  // 🔴 Close chatbot
  chatbotClose.on("click", () => chatbotContainer.addClass("hidden"));

  // ✉️ Send message
  function sendUserMessage() {
    const msg = chatInput.val().trim();
    if (!msg) return;

    // Append user message
    chatMessages.append(`<div class="message user">${msg}</div>`);
    chatInput.val("");

    // Scroll to bottom
    chatMessages.scrollTop(chatMessages[0].scrollHeight);

    // Send message to backend
    $.ajax({
      url: "/chatbot/ask",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ message: msg }),
      success: function (data) {
        chatMessages.append(`<div class="message bot">${data.reply}</div>`);
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
      },
      error: function () {
        chatMessages.append(`<div class="message bot">⚠️ Error connecting to AI assistant.</div>`);
      }
    });
  }

  // Enter key or send button
  sendMessage.on("click", sendUserMessage);
  chatInput.on("keypress", (e) => {
    if (e.which === 13) sendUserMessage();
  });
});
