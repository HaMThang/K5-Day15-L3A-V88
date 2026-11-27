# Nhiệm vụ nhánh `feat/hoang-codebase-demo` — Nguyễn Thế Hoàng (Codebase & Video Demo)

> **File độc quyền sở hữu trên nhánh này:** `codebase/agent.py`, `codebase/tools.py`, `codebase/app.py`, `codebase/ai.py`, `codebase/web/*` *(đã kéo sẵn vào nhánh này)*, `data/build_index.py`, `data/kb_index.json`, `reflection/nguyen-the-hoang.md`, `docs/tasks/hoang.md`.
> **TUYỆT ĐỐI KHÔNG SỬA:** `codebase/tracing.py`, `run.py`, `eval/metric_spec.yaml`, `spec.md`.

## 1. Cấu hình `.env` trên máy (không bao giờ commit `.env`)
```ini
MODEL_PROVIDER=anthropic
MODEL_NAME=claude-haiku-5-5
API_KEY=<key Anthropic của nhóm>
```
Kiểm tra ngay bằng:
```powershell
python run.py eval --try 3
```
*(Thấy `tokens_in > 0` và `tokens_out > 0` là xong).*

## 2. Việc cần hoàn thành trước CP3 (09:00 sáng Thứ Bảy 28/11 — hạn nộp Form 2: 10:00)
- [ ] **Quay Video 30 giây AI thật chạy (BẮT BUỘC CP3):**
  - Mở `python run.py` (hoặc Web UI nếu tích hợp xong), gõ 1 câu hỏi thật (ví dụ câu xung đột lộ trình Day14 `B08` hoặc chuyển mức `/3` hỏi hướng dẫn sửa lỗi), quay màn hình thấy rõ câu trả lời sinh ra kèm dòng `(model: claude-haiku-5-5 · gọi model 1 lần · công cụ 2 lần · token vào ... / ra ...)`.
  - Upload lên YouTube chế độ **Không công khai (Unlisted)** hoặc Google Drive (*Anyone with the link can view*), mở thử bằng **cửa sổ ẩn danh (Incognito)** rồi gửi link cho Hưng trước **09:00 sáng 28/11**.
- [ ] **(Tuỳ chọn nhưng ăn điểm cao) Nối `codebase/web/` vào `codebase/app.py`:**
  - Thư mục `codebase/web/` (`index.html`, `app.js`, `style.css`) đã được chép sẵn sang nhánh này. Bạn có thể thêm tuỳ chọn khởi chạy `http.server` chuẩn của Python trong `codebase/app.py` (ví dụ khi chạy `python codebase/app.py --web`) gọi vào `answer(text)` kèm chọn 3 mức `giai_thich | goi_y | cam_tay` và ô nhập đường dẫn `repo_path`. Giữ mặc định `python run.py` luôn hoạt động mượt trên Windows/macOS.
- [ ] **Ghim mã phiên bản / hash tài liệu trong `data/build_index.py` & `data/kb_index.json`:**
  - Bổ sung trường `doc_sha256` ngắn (8 ký tự) cho mỗi mục trong `kb_index.json` để xử lý rủi ro tài liệu lab bị sửa đổi giữa chừng.
- [ ] **Lưu ý quan trọng khi chạy `eval`:** Khi để Cương chạy `python run.py eval` chính thức, **không đặt biến `LAB_REPO_PATH`** để mọi mã trích dẫn đều thuộc tập `K5-DayXX/FILE#mục` trong `data/kb_index.json` (khớp 100% chuẩn "đạt" đã khóa).

## 3. Việc cần hoàn thành cho CP4 (10:00 → 13:00 Thứ Bảy 28/11)
- [ ] Cùng Cương đọc các câu bị trượt ở `eval/run-1.csv`, gom nhóm lỗi và thực hiện **đúng 1 đợt cải tiến có chủ đích** trong `codebase/agent.py` / `codebase/tools.py` nhắm vào nhóm lỗi đau nhất với người dùng, sau đó merge để Cương chạy `eval/run-2.csv`.

## 4. Trước khóa repo 23:59 Thứ Bảy 28/11
- [ ] Tự viết 3–6 dòng/câu vào `reflection/nguyen-the-hoang.md` (phải nắm rõ luồng 4 bước, BM25 kéo `conflicts_with`, và 3 chốt chặn hậu kiểm để trả lời Q&A).
