/* ═══════════════════════════════════════
   Copy Prompt Logic
   ═══════════════════════════════════════ */

function copyPrompt(btn) {
  const container = btn.closest(".prompt-block-enhanced");
  const content = container.querySelector(".prompt-content").innerText;

  navigator.clipboard.writeText(content).then(() => {
    // 视觉反馈
    const originalIcon = btn.innerHTML;
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4CAF50" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>';
    
    setTimeout(() => {
      btn.innerHTML = originalIcon;
    }, 2000);
  }).catch(err => {
    console.error('无法复制: ', err);
  });
}

/* ═══════════════════════════════════════
   AI Chat Widget Logic (Original)
   ═══════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", function() {
  const chatBtn = document.getElementById("ai-chat-btn");
  const chatPanel = document.getElementById("ai-chat-panel");
  const chatClose = document.getElementById("ai-chat-close");
  const chatInput = document.getElementById("ai-chat-input");
  const chatSend = document.getElementById("ai-chat-send");
  const chatMessages = document.getElementById("ai-chat-messages");

  if (!chatBtn) return;

  chatBtn.onclick = () => {
    chatPanel.classList.toggle("open");
    chatBtn.classList.toggle("hidden");
  };

  chatClose.onclick = () => {
    chatPanel.classList.remove("open");
    chatBtn.classList.remove("hidden");
  };

  const addMessage = (text, isUser = false) => {
    const msg = document.createElement("div");
    msg.className = `ai-chat-msg ${isUser ? 'ai-chat-user' : 'ai-chat-assistant'}`;
    msg.innerText = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  const handleSend = () => {
    const text = chatInput.value.trim();
    if (!text) return;
    addMessage(text, true);
    chatInput.value = "";
    
    // 模拟回复
    setTimeout(() => {
      addMessage("你好！我是 Openresource-Wiki 的智能助手。目前我正在学习博主的全部内容，很快就能为你提供更精准的解答了。");
    }, 800);
  };

  chatSend.onclick = handleSend;
  chatInput.onkeypress = (e) => { if(e.key === 'Enter') handleSend(); };
});
