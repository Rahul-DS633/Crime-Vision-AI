/**
 * CrimeVision AI - Chat Handler
 * Matches specification from Activity 4.2 / Milestone 5 (Page 15)
 */
class ChatHandler {
  constructor(mode, inputId, sendBtnId, historyId) {
    this.mode = mode;
    this.inputEl = document.getElementById(inputId);
    this.sendBtn = document.getElementById(sendBtnId);
    this.historyEl = document.getElementById(historyId);
    this.sessionId = null;

    this.init();
  }

  init() {
    if (this.sendBtn && this.inputEl) {
      this.sendBtn.addEventListener('click', () => this.sendMessage());
      this.inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          this.sendMessage();
        }
      });
    }
  }

  setSessionId(sessionId) {
    this.sessionId = sessionId;
  }

  async sendMessage() {
    const question = this.inputEl.value.trim();
    if (!question) return;

    this.addMessage('user', question); // Show user message
    this.inputEl.value = '';

    // Show temporary typing indicator
    const typingId = this.addTypingIndicator();

    try {
      const result = await API.chat(this.mode, this.sessionId, question);
      this.removeTypingIndicator(typingId);

      if (result.status === 'success') {
        this.addMessage('ai', result.answer); // Show AI forensic answer
      } else {
        this.addMessage('ai', result.message || "Information not found.");
      }
    } catch (error) {
      this.removeTypingIndicator(typingId);
      this.addMessage('ai', "Error connecting to analysis server.");
    }
  }

  addMessage(role, text) {
    if (!this.historyEl) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${role}-msg`;

    if (role === 'ai') {
      msgDiv.innerHTML = `
        <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="msg-body">${this.escapeHtml(text)}</div>
      `;
    } else {
      msgDiv.innerHTML = `
        <div class="msg-body">${this.escapeHtml(text)}</div>
      `;
    }

    this.historyEl.appendChild(msgDiv);
    this.historyEl.scrollTop = this.historyEl.scrollHeight;
  }

  addTypingIndicator() {
    const id = `typing_${Date.now()}`;
    const msgDiv = document.createElement('div');
    msgDiv.id = id;
    msgDiv.className = `chat-msg ai-msg`;
    msgDiv.innerHTML = `
      <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
      <div class="msg-body font-mono text-dim"><i class="fa-solid fa-circle-notch fa-spin"></i> Analyzing evidence context...</div>
    `;
    this.historyEl.appendChild(msgDiv);
    this.historyEl.scrollTop = this.historyEl.scrollHeight;
    return id;
  }

  removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  escapeHtml(str) {
    if (!str && str !== 0) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');
  }
}

window.ChatHandler = ChatHandler;
