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

// Markdown tối giản và an toàn: escape HTML trước, chỉ hỗ trợ đoạn văn, danh sách, trích dẫn, `code`, **đậm**.
const CODE_RE = /\[?\b([A-Za-z0-9_.-]+\/[A-Za-z0-9_./-]+#[A-Za-z0-9_-]+)\b\]?/g;
const FILE_LINE_RE = /\b([A-Za-z0-9_./-]+\.(?:md|py|json|yaml|yml|csv|txt)(?::\d+(?:[-,]\d+)*)?)/g;

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, ch => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[ch]));
}

function inline(text) {
  return text.split(/(`[^`\n]+`)/).map(piece => {
    if (/^`[^`]+`$/.test(piece)) return '<code>' + escapeHtml(piece.slice(1, -1)) + '</code>';
    return escapeHtml(piece)
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(CODE_RE, '<code>$1</code>')
      .replace(FILE_LINE_RE, (m, f, off, all) => /<code>[^<]*$/.test(all.slice(0, off)) ? m : '<code>' + f + '</code>');
  }).join('');
}

function renderMarkdown(text) {
  const html = [];
  let list = null;
  let para = [];
  let quote = [];
  const flushPara = () => { if (para.length) { html.push('<p>' + para.map(inline).join('<br>') + '</p>'); para = []; } };
  const flushList = () => { if (list) { html.push(`<${list.tag}>` + list.items.map(i => '<li>' + inline(i) + '</li>').join('') + `</${list.tag}>`); list = null; } };
  const flushQuote = () => { if (quote.length) { html.push('<blockquote>' + renderMarkdown(quote.join('\n')) + '</blockquote>'); quote = []; } };
  for (const raw of text.replace(/\r/g, '').split('\n')) {
    const line = raw.trim();
    const q = /^>\s?(.*)$/.exec(line);
    if (q) { flushPara(); flushList(); quote.push(q[1]); continue; }
    flushQuote();
    const li = /^([-*•]|\d+[.)])\s+(.*)$/.exec(line);
    if (li) {
      flushPara();
      const tag = /\d/.test(li[1]) ? 'ol' : 'ul';
      if (!list || list.tag !== tag) { flushList(); list = {tag, items: []}; }
      list.items.push(li[2]);
      continue;
    }
    if (!line) { flushPara(); flushList(); continue; }
    if (list && /^\s{2,}/.test(raw)) { list.items[list.items.length - 1] += ' ' + line; continue; }
    flushList();
    para.push(line.replace(/^#{1,6}\s+/, ''));
  }
  flushPara(); flushList(); flushQuote();
  return html.join('');
}

function addResponse(text) {
  const message = document.createElement('div');
  message.className = 'assistant-message message';
  const heading = document.createElement('span');
  heading.className = 'message-label';
  heading.textContent = '✳ LAB COMPASS';
  const bubble = document.createElement('div');
  bubble.className = 'bubble response-bubble markdown';
  bubble.innerHTML = renderMarkdown(text);
  message.append(heading, bubble);
  conversation.append(message);
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
      body: JSON.stringify({question: current, mode: mode.value, repo_path: repoPath.value}),
    });
    const data = await response.json().catch(() => ({}));
    if (response.status === 429) {
      const wait = Number(response.headers.get('Retry-After') || data.retry_after || 0);
      const when = wait ? ` Bạn thử lại sau khoảng ${wait >= 60 ? Math.ceil(wait / 60) + ' phút' : wait + ' giây'} nhé.` : ' Bạn đợi một lát rồi thử lại nhé.';
      throw new Error((data.error || 'Bản demo đang giới hạn số lượt hỏi.') + when);
    }
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
    const offline = error instanceof TypeError; // fetch() ném TypeError khi mất kết nối tới server
    addMessage('✳ LAB COMPASS', offline || !error.message ? 'Mình chưa kết nối được tới máy chủ. Bạn kiểm tra mạng rồi gửi lại nhé, câu hỏi vẫn còn trong ô nhập.' : error.message);
    question.value = current;
    question.dispatchEvent(new Event('input'));
    status.textContent = 'Bạn có thể sửa hoặc gửi lại câu hỏi.';
  } finally {
    submit.disabled = false;
    reset.disabled = false;
    submit.innerHTML = 'Gửi câu hỏi <span>→</span>';
    question.focus();
    // Đưa đầu câu trả lời mới lên trên để học viên đọc từ câu đầu, không phải từ cuối.
    const last = [...conversation.querySelectorAll('.assistant-message')].pop();
    conversation.scrollTop = last ? last.offsetTop - conversation.offsetTop - 8 : conversation.scrollHeight;
  }
});
