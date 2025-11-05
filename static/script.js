// State Management
const state = {
  sessionId: null,
  isLoading: false,
  theme: localStorage.getItem("theme") || "light",
  attachedFile: null,
  systemStatus: null,
  widgetState: localStorage.getItem("widgetState") || "icon", // icon, popup, fullscreen
};

// API Configuration
const API_BASE_URL = "http://localhost:8000/api/v1";

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initWidgetState();
  initEventListeners();
  checkSystemStatus();
  autoResizeTextarea();
  initIframeLoading();
});

// Widget State Management
function initWidgetState() {
  // Default to icon state always - don't load from localStorage
  setWidgetState("icon");
}

function setWidgetState(newState) {
  const validStates = ["icon", "popup", "fullscreen"];
  if (!validStates.includes(newState)) {
    newState = "icon";
  }

  state.widgetState = newState;
  localStorage.setItem("widgetState", newState);

  // Update body class
  document.body.className = "";
  if (newState === "popup") {
    document.body.classList.add("chat-popup");
  } else if (newState === "fullscreen") {
    document.body.classList.add("chat-fullscreen");
  }

  // Update widget class
  const widget = document.getElementById("chatWidget");
  widget.className = "chat-widget";
  if (newState !== "icon") {
    widget.classList.add(`state-${newState}`);
  }

  // Update maximize button icon
  const maximizeBtn = document.getElementById("maximizeBtn");
  if (maximizeBtn) {
    const icon = maximizeBtn.querySelector(".material-icons");
    if (newState === "fullscreen") {
      icon.textContent = "fullscreen_exit";
      maximizeBtn.title = "Exit Fullscreen";
    } else {
      icon.textContent = "fullscreen";
      maximizeBtn.title = "Fullscreen";
    }
  }
}

function openPopup() {
  setWidgetState("popup");
}

function togglePopup() {
  if (state.widgetState === "popup") {
    setWidgetState("icon");
  } else {
    setWidgetState("popup");
  }
}

function minimizeWidget() {
  setWidgetState("icon");
}

function toggleFullscreen() {
  if (state.widgetState === "fullscreen") {
    setWidgetState("popup");
  } else {
    setWidgetState("fullscreen");
  }
}

// Theme Management
function initTheme() {
  document.documentElement.setAttribute("data-theme", state.theme);
  updateThemeIcon();
}

function toggleTheme() {
  state.theme = state.theme === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", state.theme);
  localStorage.setItem("theme", state.theme);
  updateThemeIcon();
}

function updateThemeIcon() {
  const themeIcon = document.getElementById("themeIcon");
  themeIcon.textContent = state.theme === "light" ? "dark_mode" : "light_mode";
}

// Event Listeners
function initEventListeners() {
  const messageInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");
  const themeToggle = document.getElementById("themeToggle");
  const attachBtn = document.getElementById("attachBtn");
  const fileInput = document.getElementById("fileInput");
  
  // Widget controls
  const chatFloatIcon = document.getElementById("chatFloatIcon");
  const minimizeBtn = document.getElementById("minimizeBtn");
  const maximizeBtn = document.getElementById("maximizeBtn");
  const closeBtn = document.getElementById("closeBtn");
  const exitFullscreenBtn = document.getElementById("exitFullscreenBtn");

  messageInput.addEventListener("keydown", handleKeyDown);
  messageInput.addEventListener("input", autoResizeTextarea);
  sendBtn.addEventListener("click", sendMessage);
  themeToggle.addEventListener("click", toggleTheme);

  // Widget event listeners
  chatFloatIcon.addEventListener("click", togglePopup);
  minimizeBtn.addEventListener("click", minimizeWidget);
  maximizeBtn.addEventListener("click", toggleFullscreen);
  closeBtn.addEventListener("click", minimizeWidget);
  exitFullscreenBtn.addEventListener("click", () => setWidgetState("popup"));

  // File attachment (for future use)
  if (attachBtn) {
    attachBtn.addEventListener("click", () => {
      showToast("File attachment feature coming soon!", "info", "attach_file");
      // fileInput.click(); // Enable when ready
    });
  }

  if (fileInput) {
    fileInput.addEventListener("change", handleFileSelect);
  }
  
  // Keyboard shortcuts
  document.addEventListener("keydown", handleGlobalKeyDown);
}

function handleGlobalKeyDown(event) {
  // ESC key to minimize widget
  if (event.key === "Escape") {
    if (state.widgetState === "fullscreen") {
      setWidgetState("popup");
    } else if (state.widgetState === "popup") {
      minimizeWidget();
    }
  }
}

function handleKeyDown(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
}

function autoResizeTextarea() {
  const textarea = document.getElementById("messageInput");
  textarea.style.height = "auto";
  textarea.style.height = Math.min(textarea.scrollHeight, 128) + "px";
}

// System Status
async function checkSystemStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    state.systemStatus = data;
    updateStatusUI(data);
  } catch (error) {
    console.error("Status check failed:", error);
    updateStatusUI(null);
  }
}

function updateStatusUI(status) {
  const indicator = document.getElementById("statusIndicator");
  const content = document.getElementById("statusContent");

  if (!status) {
    indicator.classList.add("offline");
    content.innerHTML = `
      <div class="status-item">
        <span>Status</span>
        <span class="status-badge offline">Offline</span>
      </div>
    `;
    return;
  }

  indicator.classList.remove("offline");

  const providers = status.available_providers || {};
  const providerList = Object.entries(providers)
    .map(
      ([name, available]) => `
      <div class="status-item">
        <span>${name.charAt(0).toUpperCase() + name.slice(1)}</span>
        <span class="status-badge ${available ? "online" : "offline"}">
          ${available ? "✓ Available" : "✗ Unavailable"}
        </span>
      </div>
    `
    )
    .join("");

  content.innerHTML = `
    <div class="status-item">
      <span>Status</span>
      <span class="status-badge online">Online</span>
    </div>
    <div class="status-item">
      <span>Version</span>
      <span>${status.version || "N/A"}</span>
    </div>
    <div class="status-item">
      <span>Active Provider</span>
      <span>${status.model_provider || "N/A"}</span>
    </div>
    ${providerList}
  `;
}

// Chat Functions
function sendQuickQuestion(question) {
  document.getElementById("messageInput").value = question;
  sendMessage();
}

async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();

  if (!message || state.isLoading) return;

  state.isLoading = true;
  updateSendButton(true);

  // Add user message
  addMessage("user", message);
  input.value = "";
  autoResizeTextarea();

  // Show typing indicator
  const typingId = addTypingIndicator();

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
        session_id: state.sessionId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // Store session ID
    if (data.session_id && !state.sessionId) {
      state.sessionId = data.session_id;
    }

    // Remove typing indicator
    removeTypingIndicator(typingId);

    // Add bot response with metadata
    const metadata = {
      provider: data.provider || "N/A",
      model: data.model || "N/A",
      cost: data.cost || "N/A",
      time: data.processing_time || "N/A",
    };
    addMessage("bot", data.response, metadata);
  } catch (error) {
    console.error("Chat error:", error);
    removeTypingIndicator(typingId);

    addMessage(
      "bot",
      "I apologize, but I'm having trouble connecting to the backend service. Please ensure the server is running and try again.",
      { provider: "Error", model: "N/A", cost: "N/A", time: "N/A" }
    );

    showToast(
      "Failed to send message. Please check your connection.",
      "error"
    );
  } finally {
    state.isLoading = false;
    updateSendButton(false);
  }
}

function addMessage(type, content, metadata = null) {
  const chatArea = document.getElementById("chatArea");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  const avatarIcon = document.createElement("span");
  avatarIcon.className = "material-icons";
  avatarIcon.textContent = type === "user" ? "account_circle" : "smart_toy";
  avatar.appendChild(avatarIcon);

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";

  const textDiv = document.createElement("div");
  
  // Format message content (support markdown-style formatting)
  const formattedContent = formatMessageContent(content);
  textDiv.innerHTML = formattedContent;
  contentDiv.appendChild(textDiv);

  // Add metadata tooltip for bot messages
  if (type === "bot" && metadata) {
    const metadataDiv = document.createElement("div");
    metadataDiv.className = "message-metadata";
    metadataDiv.innerHTML = `
      <div class="metadata-item">
        <span>Provider:</span>
        <span>${metadata.provider}</span>
      </div>
      <div class="metadata-item">
        <span>Model:</span>
        <span>${metadata.model}</span>
      </div>
      ${
        metadata.cost && metadata.cost !== "N/A"
          ? `<div class="metadata-item">
        <span>Cost:</span>
        <span>${metadata.cost}</span>
      </div>`
          : ""
      }
      ${
        metadata.time && metadata.time !== "N/A"
          ? `<div class="metadata-item">
        <span>Time:</span>
        <span>${metadata.time}s</span>
      </div>`
          : ""
      }
    `;
    contentDiv.appendChild(metadataDiv);
  }

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(contentDiv);
  chatArea.appendChild(messageDiv);

  // Smooth scroll to bottom
  chatArea.scrollTo({
    top: chatArea.scrollHeight,
    behavior: "smooth",
  });
}

function addTypingIndicator() {
  const chatArea = document.getElementById("chatArea");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot";
  messageDiv.id = "typing-indicator";

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  const avatarIcon = document.createElement("span");
  avatarIcon.className = "material-icons";
  avatarIcon.textContent = "smart_toy";
  avatar.appendChild(avatarIcon);

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.innerHTML = `
    <div class="typing-indicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>
  `;

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(contentDiv);
  chatArea.appendChild(messageDiv);

  chatArea.scrollTo({
    top: chatArea.scrollHeight,
    behavior: "smooth",
  });

  return "typing-indicator";
}

function removeTypingIndicator(id) {
  const indicator = document.getElementById(id);
  if (indicator) {
    indicator.remove();
  }
}

function updateSendButton(loading) {
  const sendBtn = document.getElementById("sendBtn");
  const btnText = document.getElementById("sendBtnText");

  sendBtn.disabled = loading;

  if (loading) {
    btnText.innerHTML = '<div class="spinner"></div>';
  } else {
    const icon = document.createElement("span");
    icon.className = "material-icons";
    icon.textContent = "send";
    btnText.innerHTML = "";
    btnText.appendChild(icon);
  }
}

// File Handling (for future PDF support)
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;

  state.attachedFile = file;
  showFilePreview(file);
  showToast(`File "${file.name}" attached`, "success");
}

function showFilePreview(file) {
  const container = document.getElementById("filePreviewContainer");
  container.innerHTML = `
    <div class="file-preview">
      <span class="material-icons">attach_file</span>
      <span>${file.name}</span>
      <button class="file-preview-remove" onclick="removeFile()">
        <span class="material-icons">close</span>
      </button>
    </div>
  `;
}

function removeFile() {
  state.attachedFile = null;
  document.getElementById("filePreviewContainer").innerHTML = "";
  document.getElementById("fileInput").value = "";
}

// Toast Notifications
function showToast(message, type = "info", icon = null) {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;

  const icons = {
    success: "check_circle",
    error: "error",
    warning: "warning",
    info: "info",
  };

  const toastIcon = icon || icons[type] || icons.info;

  const iconSpan = document.createElement("span");
  iconSpan.className = "material-icons toast-icon";
  iconSpan.textContent = toastIcon;

  const contentDiv = document.createElement("div");
  contentDiv.className = "toast-content";

  const titleDiv = document.createElement("div");
  titleDiv.className = "toast-title";
  titleDiv.textContent = type.charAt(0).toUpperCase() + type.slice(1);

  const messageDiv = document.createElement("div");
  messageDiv.className = "toast-message";
  messageDiv.textContent = message;

  contentDiv.appendChild(titleDiv);
  contentDiv.appendChild(messageDiv);

  const closeBtn = document.createElement("button");
  closeBtn.className = "toast-close";
  closeBtn.onclick = () => toast.remove();
  const closeIcon = document.createElement("span");
  closeIcon.className = "material-icons";
  closeIcon.textContent = "close";
  closeBtn.appendChild(closeIcon);

  toast.appendChild(iconSpan);
  toast.appendChild(contentDiv);
  toast.appendChild(closeBtn);

  container.appendChild(toast);

  // Auto remove after 5 seconds
  setTimeout(() => {
    toast.style.animation = "toastSlideIn 0.3s reverse";
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

// Utility Functions
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function formatMessageContent(content) {
  // Escape HTML first
  let formatted = escapeHtml(content);
  
  // Format bold text (**text** -> <strong>text</strong>)
  formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Format bullet points (• or - at start of line)
  formatted = formatted.replace(/^[•\-]\s+(.+)$/gm, '<div style="margin-left: 20px;">• $1</div>');
  
  // Format numbered lists
  formatted = formatted.replace(/^(\d+)\.\s+(.+)$/gm, '<div style="margin-left: 20px;">$1. $2</div>');
  
  // Format section headers (🎯, 📋, ✅, 📌, 💡, etc. at start)
  formatted = formatted.replace(/^([🎯📋✅📌💡🥇🥈🥉📊💰🛡️]+)\s+\*\*([^*]+)\*\*/gm, 
    '<div style="margin-top: 12px; margin-bottom: 8px; font-weight: bold;">$1 $2</div>');
  
  // Format question numbers (e.g., "Question 1 of 5")
  formatted = formatted.replace(/\*\*Question\s+(\d+)\s+of\s+(\d+)\*\*/g, 
    '<div style="background: var(--primary-color); color: white; padding: 8px 12px; border-radius: 8px; margin: 8px 0; display: inline-block;"><strong>Question $1 of $2</strong></div>');
  
  // Convert newlines to <br>
  formatted = formatted.replace(/\n/g, '<br>');
  
  // Fix nested <div> issues by removing <br> before closing </div>
  formatted = formatted.replace(/<br><\/div>/g, '</div>');
  
  return formatted;
}

// Periodic status check
setInterval(checkSystemStatus, 30000); // Check every 30 seconds

// Iframe Loading Management
function initIframeLoading() {
  const iframe = document.getElementById('backgroundWebsite');
  const chatFloatIcon = document.getElementById('chatFloatIcon');
  
  // Show icon after iframe loads
  iframe.addEventListener('load', () => {
    setTimeout(() => {
      chatFloatIcon.classList.add('loaded');
    }, 500); // Small delay for smooth appearance
  });
  
  // Fallback: show icon after 3 seconds if iframe doesn't load
  setTimeout(() => {
    if (!chatFloatIcon.classList.contains('loaded')) {
      chatFloatIcon.classList.add('loaded');
    }
  }, 3000);
}
