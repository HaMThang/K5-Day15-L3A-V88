const form = document.querySelector('#question-form');
const question = document.querySelector('#question');
const count = document.querySelector('#count');
const submit = document.querySelector('#submit');
const status = document.querySelector('#status');
const conversation = document.querySelector('#conversation');
const reset = document.querySelector('#reset');
const examples = document.querySelector('.examples');
const mode = document.querySelector('#mode');
const repoPath = document.querySelector('#repo-path');
const pickLab = document.querySelector('#pick-lab');
const labFiles = document.querySelector('#lab-files');
const labChosen = document.querySelector('#lab-chosen');
const clearLab = document.querySelector('#clear-lab');

// Lọc giống codebase/tools.py: chỉ file văn bản, bỏ thư mục ẩn/ảo và file bí mật.
const SKIP_DIRS = new Set(['.git', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache', '.mypy_cache',
  'data-btc', '.idea', '.vscode', '.claude', '.gemini', '.codex']);
const ALLOWED_EXTS = new Set(['.md', '.py', '.yaml', '.yml', '.toml', '.txt']);
let limits = {max_files: 60, max_file_bytes: 48000};
let labId = '';
const NO_LAB = 'Chưa chọn · dùng chỉ mục 12 bài Lab K5';

function isSecret(name) {
  const low = name.toLowerCase();
  if (low === '.env' || (low.startsWith('.env.') && low !== '.env.example')) return true;
  return /\.(pem|key|pfx)$/.test(low) || low.includes('credentials') || low.includes('secret');
}

function setLab(id, label) {
  labId = id;
  labChosen.textContent = label || NO_LAB;
  clearLab.hidden = !id;
}

fetch('/api/config').then(r => r.json()).then(cfg => {
  limits = cfg;
  repoPath.hidden = !cfg.allow_repo_path;
}).catch(() => {});

pickLab.addEventListener('click', () => labFiles.click());
clearLab.addEventListener('click', () => { setLab('', ''); labFiles.value = ''; });
labFiles.addEventListener('change', async () => {
  const all = [...labFiles.files];
  if (!all.length) return;
  const root = all[0].webkitRelativePath.split('/')[0] || 'lab';
  const picked = all.map(file => ({file, parts: file.webkitRelativePath.split('/').slice(1)})).filter(({file, parts}) => {
    if (!parts.length) return false;
    if (parts.slice(0, -1).some(dir => SKIP_DIRS.has(dir) || dir.startsWith('.'))) return false;
    const name = parts[parts.length - 1];
    const dot = name.lastIndexOf('.');
    return dot > 0 && ALLOWED_EXTS.has(name.slice(dot).toLowerCase()) && !isSecret(name) && file.size <= limits.max_file_bytes;
  });
  // Ưu tiên file .md và file ở gần thư mục gốc, vì tài liệu yêu cầu bài lab thường nằm ở đó.
  picked.sort((a, b) => (a.parts.at(-1).toLowerCase().endsWith('.md') ? 0 : 1) - (b.parts.at(-1).toLowerCase().endsWith('.md') ? 0 : 1)
    || a.parts.length - b.parts.length || a.parts.join('/').localeCompare(b.parts.join('/')));
  const chosen = picked.slice(0, limits.max_files);
  if (!chosen.length) {
    setLab('', 'Thư mục không có file .md/.py/.yaml/.txt phù hợp');
    labFiles.value = '';
    return;
  }
  pickLab.disabled = true;
  labChosen.textContent = `Đang gửi ${chosen.length} file…`;
  try {
    const files = await Promise.all(chosen.map(async ({file, parts}) => ({path: parts.join('/'), content: await file.text()})));
    const response = await fetch('/api/upload_lab', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name: root, files}),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Không gửi được thư mục.');
    const left = all.length - data.files;
    setLab(data.lab_id, `${data.name} · ${data.files} file${left > 0 ? ` (bỏ qua ${left})` : ''} · hết hạn sau ${data.ttl_minutes} phút`);
    repoPath.value = '';
  } catch (error) {
    setLab('', error.message || 'Không gửi được thư mục.');
  } finally {
    pickLab.disabled = false;
    labFiles.value = '';
  }
});

function addMessage(label, text, role = 'assistant') {
  const message = document.createElement('div');
  message.className = role + '-message message';
  const heading = document.createElement('span');
  heading.className = 'message-label';
  heading.textContent = label;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  message.append(heading, bubble);
  conversation.append(message);
}

function splitResponse(text) {
  const lines = text.split(/\n+/).map(line => line.trim()).filter(Boolean);
  const parts = [];
  for (const line of lines) {
    if (line.length > 300 && !line.startsWith('- Nguồn') && !line.startsWith('[')) {
      const sentences = line.split(/(?<=[.!?])\s+(?=[A-ZÀ-Ỹ])/u);
      if (sentences && sentences.length > 1) {
        let chunk = '';
        for (const sentence of sentences) {
          const next = sentence.trim();
          if (chunk && chunk.length + next.length > 260) {
            parts.push(chunk);
            chunk = '';
          }
          chunk += (chunk ? ' ' : '') + next;
        }
        if (chunk) parts.push(chunk);
        continue;
      }
    }
    parts.push(line);
  }
  return parts;
}

function addResponse(text) {
  const parts = splitResponse(text);
  const isSource = part => /^-\s*Nguồn(?:\s|:)/iu.test(part);
  const sources = parts.filter(isSource);
  const answers = parts.filter(part => !isSource(part));
  if (!answers.length && sources.length) answers.push('Nguồn tài liệu:');
  answers.forEach((part, index) => {
    const message = document.createElement('div');
    message.className = 'assistant-message message';
    if (index === 0) {
      const heading = document.createElement('span');
      heading.className = 'message-label';
      heading.textContent = '✳ LAB COMPASS';
      message.append(heading);
    }
    const bubble = document.createElement('div');
    bubble.className = 'bubble response-bubble';
    const section = document.createElement('div');
    section.className = 'response-part';
    section.textContent = part;
    bubble.append(section);
    if (index === 0) {
      sources.forEach(source => {
        const reference = document.createElement('div');
        reference.className = 'response-part response-source';
        reference.textContent = source;
        bubble.append(reference);
      });
    }
    message.append(bubble);
    conversation.append(message);
  });
}

question.addEventListener('input', () => { count.textContent = question.value.length + ' / 1500'; });
document.querySelectorAll('.example').forEach(button => button.addEventListener('click', () => {
  question.value = button.dataset.question;
  question.dispatchEvent(new Event('input'));
  question.focus();
}));
reset.addEventListener('click', () => {
  conversation.replaceChildren();
  addMessage('✳ LAB COMPASS', 'Chào bạn! Hãy cho mình biết ngày lab và checkpoint bạn đang vướng nhé.');
  question.value = '';
  question.dispatchEvent(new Event('input'));
  status.textContent = '';
  examples.hidden = false;
  question.focus();
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  const current = question.value.trim();
  if (!current || submit.disabled) return;
  addMessage('BẠN', current, 'user');
  question.value = '';
  question.dispatchEvent(new Event('input'));
  submit.disabled = true;
  reset.disabled = true;
  submit.textContent = 'Đang tra cứu…';
  status.textContent = 'Đang tìm tài liệu và chuẩn bị câu trả lời…';
  examples.hidden = true;
  try {
    const response = await fetch('/api/answer', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: current, mode: mode.value, repo_path: labId ? '' : repoPath.value, lab_id: labId}),
    });
    const data = await response.json();
    if (data.lab_expired) setLab('', 'Thư mục đã hết hạn · hãy chọn lại');
    if (!response.ok) throw new Error(data.error || 'Không thể tra cứu lúc này.');
    addResponse(data.output);
    const details = document.createElement('div');
    details.className = 'conversation-meta';
    details.textContent = `Model: ${data.model || '—'} · gọi model ${data.model_calls} lần · công cụ ${data.tool_calls} lần · token vào ${data.tokens_in} / ra ${data.tokens_out}`;
    const copy = document.createElement('button');
    copy.type = 'button';
    copy.className = 'copy';
    copy.textContent = 'Sao chép câu trả lời';
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(data.output);
        copy.textContent = 'Đã sao chép';
        setTimeout(() => { copy.textContent = 'Sao chép câu trả lời'; }, 2000);
      } catch (_) { copy.textContent = 'Không sao chép được'; }
    });
    details.append(' ', copy);
    conversation.append(details);
    status.textContent = '';
  } catch (error) {
    addMessage('✳ LAB COMPASS', error.message || 'Không thể kết nối. Hãy thử lại.');
    question.value = current;
    question.dispatchEvent(new Event('input'));
    status.textContent = 'Bạn có thể sửa hoặc gửi lại câu hỏi.';
  } finally {
    submit.disabled = false;
    reset.disabled = false;
    submit.innerHTML = 'Gửi câu hỏi <span>→</span>';
    question.focus();
    conversation.scrollTop = conversation.scrollHeight;
  }
});
