# Reflection — Nguyễn Thế Hoàng (2A202603718)

> Hạn hoàn thành: **23:59 Thứ Bảy 28/11/2026**.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Vai trò: Phụ trách bản chạy thử `codebase/` (`ai.py`, `tools.py`, `agent.py`, `app.py`, `web/`) và chỉ mục `data/build_index.py` → `data/kb_index.json`, nối API model thật và quay video demo 30 giây.
   - Luồng trong `codebase/agent.py` có bốn bước: nhận diện mức hướng dẫn và tín hiệu từ câu hỏi, truy xuất tài liệu chỉ đọc, gọi model một lần, rồi hậu kiểm bằng code.
   - `codebase/tools.py` dùng BM25 để xếp hạng đoạn liên quan và kéo thêm nguồn đối chiếu qua `conflicts_with`. Với Day14, cách này đưa cả lộ trình 335 phút trong `CODE_LAB` và lộ trình 240 phút trong `CHECKPOINTS` vào ngữ cảnh.
   - Commit `5ba5fc9` thêm giao diện Web. Phần nối `codebase/app.py` với Web UI và bổ sung hash trong `data/kb_index.json` đang ở nhánh local. Video demo 30 giây đã được ghi link trong `docs/tasks/hoang.md`.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng Codex để nối Web UI với `answer()`, thêm SHA-256 rút gọn và dựng clip demo. Khi thiếu tài liệu gốc, phần tạo chỉ mục ghi rõ hash nào thuộc file nguồn và hash nào thuộc bản trích.
   - Phần mình cần nắm khi review là ba chốt hậu kiểm: chặn yêu cầu làm hộ hoặc chạy lệnh thay học viên, xác minh mã trích dẫn, và nêu giới hạn kèm câu hỏi nháp cho Lab Coach khi nguồn thiếu hoặc mâu thuẫn.
   - Sau khi mình thêm API key, `python run.py eval --try 3` ghi nhận cả 3 câu trả token vào và ra từ Claude Haiku 5.5 trong `eval/run-try.csv`. Clip Day14 cho thấy phản hồi có cả hai mã trích dẫn.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - B01 từng lỗi kỹ thuật ở lượt thử `python run.py eval --try 3` do thiếu `API_KEY`. Sau khi thêm key và chạy lại với kết nối mạng tới Anthropic, B01 trả 5.767 token vào và 989 token ra, ghi trong `eval/run-try.csv`.
   - Bài học là phải kiểm cột `error` và số token trước khi chấm nội dung. Lượt gọi thành công xác nhận kết nối API, còn cột `pass` cần được chấm theo tiêu chí của từng câu.
   - Kết quả chính thức CHƯA KIỂM vì workspace chưa có `eval/run-1.csv` và `eval/run-2.csv`. Khi có dữ liệu, mình sẽ đối chiếu một câu trượt, xác định nguyên nhân và ghi kết quả sau đợt cải tiến.
