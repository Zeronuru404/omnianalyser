// OmniAnalyser Frontend
const API = '/api';
let uploadedFiles = [];
let analysisResults = [];
let lastContext = '';

// Tab navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = link.dataset.tab;
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        link.classList.add('active');
        document.getElementById('tab-' + tab).classList.add('active');
        if (tab === 'dashboard') refreshDashboard();
    });
});

// Drag & drop
const dropzone = document.getElementById('dropzone');
dropzone.addEventListener('click', () => document.getElementById('fileInput').click());
dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});
document.getElementById('fileInput').addEventListener('change', (e) => handleFiles(e.target.files));

function handleFiles(files) {
    for (const file of files) {
        uploadedFiles.push(file);
    }
    renderQueue();
}

function renderQueue() {
    const section = document.getElementById('queueSection');
    const queue = document.getElementById('fileQueue');
    if (uploadedFiles.length === 0) { section.style.display = 'none'; return; }
    section.style.display = 'block';
    queue.innerHTML = uploadedFiles.map((f, i) => `
        <div class="queue-item">
            <span class="queue-name">${f.name}</span>
            <span class="queue-size">${(f.size / 1024).toFixed(1)} KB</span>
            <span class="queue-status queue-pending" id="qs-${i}">pending</span>
        </div>
    `).join('');
}

async function runAnalysis() {
    const btn = document.getElementById('analyzeBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Analyzing...';

    for (let i = 0; i < uploadedFiles.length; i++) {
        const status = document.getElementById('qs-' + i);
        status.textContent = 'analyzing...';
        status.className = 'queue-status';
        status.style.background = '#6c5ce7';
        status.style.color = '#fff';

        try {
            const formData = new FormData();
            formData.append('file', uploadedFiles[i]);
            const resp = await fetch(API + '/analyze', { method: 'POST', body: formData });
            const data = await resp.json();
            if (data.status === 'success') {
                analysisResults.push(data.result);
                lastContext = data.result.analysis;
                status.textContent = 'done';
                status.className = 'queue-status queue-done';
            } else {
                status.textContent = 'error';
                status.style.background = '#ff7675';
            }
        } catch (err) {
            status.textContent = 'error';
            status.style.background = '#ff7675';
        }
    }

    btn.disabled = false;
    btn.textContent = '🔬 Analyze All';
    renderResults();
    refreshTokenBadge();
}

function renderResults() {
    const container = document.getElementById('resultsContainer');
    if (analysisResults.length === 0) return;
    container.innerHTML = analysisResults.map((r, i) => `
        <div class="result-card">
            <div class="result-header">
                <span class="result-filename">${r.filename}</span>
                <span class="result-agent">${r.agent}</span>
            </div>
            <div class="result-body">${markdownToHtml(r.analysis)}</div>
            <div class="result-meta">
                <span>⚡ ${r.tokens_used} tokens</span>
                <span>🤖 ${r.model}</span>
            </div>
        </div>
    `).join('');

    // Switch to results tab
    document.querySelector('[data-tab="results"]').click();
}

// Chat
async function sendChat() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    const messages = document.getElementById('chatMessages');
    messages.innerHTML += `<div class="chat-msg user"><div class="chat-bubble">${escapeHtml(msg)}</div></div>`;

    try {
        const resp = await fetch(API + '/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: msg, context: lastContext }),
        });
        const data = await resp.json();
        messages.innerHTML += `<div class="chat-msg ai"><div class="chat-bubble">${markdownToHtml(data.answer)}</div></div>`;
        lastContext = data.answer;
        refreshTokenBadge();
    } catch (err) {
        messages.innerHTML += `<div class="chat-msg ai"><div class="chat-bubble">Error: ${err.message}</div></div>`;
    }
    messages.scrollTop = messages.scrollHeight;
}

document.getElementById('chatInput')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendChat();
});

// Dashboard
async function refreshDashboard() {
    try {
        const [stats, history, agents] = await Promise.all([
            fetch(API + '/stats').then(r => r.json()),
            fetch(API + '/stats/history').then(r => r.json()),
            fetch(API + '/stats/agents').then(r => r.json()),
        ]);

        document.getElementById('statTokens').textContent = formatNumber(stats.tokens_today);
        document.getElementById('statCalls').textContent = stats.total_calls;
        document.getElementById('statFiles').textContent = analysisResults.length;
        document.getElementById('statUptime').textContent = stats.uptime_minutes + 'm';

        const budget = 10000000;
        const pct = Math.min((stats.tokens_today / budget) * 100, 100);
        document.getElementById('tokenBar').style.width = pct + '%';

        // Agent breakdown
        const agentColors = {
            code_analyzer: '#6c5ce7',
            doc_analyzer: '#00cec9',
            data_analyzer: '#fdcb6e',
            image_analyzer: '#ff7675',
            chat: '#74b9ff',
        };
        const agentBars = document.getElementById('agentBars');
        const maxTokens = Math.max(...Object.values(agents.agents || { _: 1 }), 1);
        agentBars.innerHTML = Object.entries(agents.agents || {}).map(([name, tokens]) => `
            <div class="agent-bar-row">
                <div class="agent-bar-label">${name}</div>
                <div class="agent-bar-track">
                    <div class="agent-bar-fill" style="width:${(tokens / maxTokens) * 100}%;background:${agentColors[name] || '#6c5ce7'}">${formatNumber(tokens)}</div>
                </div>
                <div class="agent-bar-value">${formatNumber(tokens)}</div>
            </div>
        `).join('');

        // Recent activity
        const recentList = document.getElementById('recentList');
        recentList.innerHTML = (stats.recent_files || []).reverse().map(r => `
            <div class="recent-item">
                <span>${r.filename || 'chat'}</span>
                <span>${r.agent}</span>
                <span style="color:var(--success)">${formatNumber(r.tokens)} tokens</span>
            </div>
        `).join('');
    } catch (err) {
        console.error('Dashboard error:', err);
    }
}

async function refreshTokenBadge() {
    try {
        const stats = await fetch(API + '/stats').then(r => r.json());
        document.getElementById('tokenCount').textContent = formatNumber(stats.tokens_today);
    } catch (err) {}
}

// Helpers
function formatNumber(n) {
    if (n >= 1e9) return (n / 1e9).toFixed(1) + 'B';
    if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
    if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
    return String(n);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function markdownToHtml(md) {
    return md
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
        .replace(/\n/g, '<br>');
}
