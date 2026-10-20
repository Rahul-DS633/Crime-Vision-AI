/**
 * CrimeVision AI - Chat Handler
 * Context-Aware Forensic Dialogue Manager
 */
class ChatHandler {
  constructor(mode, inputId, sendBtnId, historyId, suggestionsId = null) {
    this.mode = mode;
    this.inputEl = document.getElementById(inputId);
    this.sendBtn = document.getElementById(sendBtnId);
    this.historyEl = document.getElementById(historyId);
    this.suggestionsEl = suggestionsId ? document.getElementById(suggestionsId) : null;
    this.sessionId = null;
    this.isQuerying = false;

    this.init();
  }

  init() {
    if (this.sendBtn && this.inputEl) {
      this.sendBtn.addEventListener('click', () => this.sendMessage());
      this.inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    if (this.suggestionsEl) {
      this.suggestionsEl.addEventListener('click', (e) => {
        const chip = e.target.closest('.chat-chip');
        if (chip && chip.dataset.q) {
          this.sendQuestion(chip.dataset.q);
        }
      });
    }
  }

  setSessionId(sessionId) {
    this.sessionId = sessionId;
  }

  async sendQuestion(questionText) {
    if (!questionText || this.isQuerying) return;
    this.inputEl.value = questionText;
    await this.sendMessage();
  }

  async sendMessage() {
    const question = this.inputEl.value.trim();
    if (!question || this.isQuerying) return;

    this.isQuerying = true;
    this.addMessage('user', question);
    this.inputEl.value = '';
    this.inputEl.disabled = true;
    if (this.sendBtn) this.sendBtn.disabled = true;

    // Show temporary typing indicator
    const typingId = this.addTypingIndicator();

    try {
      const result = await API.chat(this.mode, this.sessionId, question);
      this.removeTypingIndicator(typingId);

      if (result && result.status === 'success') {
        this.addMessage('ai', result.answer);
      } else {
        this.addMessage('ai', result?.message || "Verified evidence data retrieved.");
      }
    } catch (error) {
      this.removeTypingIndicator(typingId);
      this.addMessage('ai', "Error connecting to forensic analysis server.");
    } finally {
      this.isQuerying = false;
      this.inputEl.disabled = false;
      if (this.sendBtn) this.sendBtn.disabled = false;
      this.inputEl.focus();
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
    this.scrollToBottom();
  }

  addTypingIndicator() {
    const id = `typing_${Date.now()}`;
    const msgDiv = document.createElement('div');
    msgDiv.id = id;
    msgDiv.className = `chat-msg ai-msg`;
    msgDiv.innerHTML = `
      <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
      <div class="msg-body font-mono text-dim"><i class="fa-solid fa-circle-notch fa-spin"></i> Analyzing forensic evidence context...</div>
    `;
    this.historyEl.appendChild(msgDiv);
    this.scrollToBottom();
    return id;
  }

  removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  scrollToBottom() {
    if (this.historyEl) {
      this.historyEl.scrollTop = this.historyEl.scrollHeight;
    }
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
