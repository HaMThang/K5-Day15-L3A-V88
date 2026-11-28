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
      body: JSON.stringify({question: current, mode: mode.value, repo_path: repoPath.value}),
    });
    const data = await response.json();
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
