# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Nghiên cứu so sánh giải pháp (`docs/research/`) | Claude, Antigravity (Gemini) | Tổng hợp tài liệu học thuật, so sánh ChatGPT/NotebookLM, nháp khung trả lời | Hưng đọc kiểm từng nguồn trích dẫn, kiểm tra commit `6225f90` và chốt kiến trúc | Lê Gia Hưng |
| Code bản chạy thử (`codebase/`, `data/build_index.py`) | Antigravity (Gemini), Claude Code | Viết hàm BM25 `search_docs`, `get_section`, `draft_coach_question`, HTTP client `ai.py` và bộ hậu kiểm `agent.py` | Hoàng đọc kiểm toàn bộ luồng, chạy thử từng nhánh (`fake` và model thật), kiểm soát điều kiện dừng & guardrail | Nguyễn Thế Hoàng |
| Prompt / thiết kế lời gọi mô hình | Antigravity (Gemini), Claude | Đề xuất cấu trúc XML tag chống prompt injection và schema JSON đầu ra | Hoàng & Hưng rà lại luật từ chối làm hộ và cách xử lý câu mâu thuẫn | Nguyễn Thế Hoàng, Lê Gia Hưng |
| Đào data (`evidence/count_preclass.py`) | Antigravity (Gemini) | Viết script Python đếm lại sự kiện trong `data/preclass/` | Thắng kiểm tay ≥10 dòng gốc đối chiếu với kết quả script in ra | Hà Minh Thắng |
| Rà câu hỏi phỏng vấn / khảo sát | Claude | Gợi ý 5 câu hỏi kiểu Mom Test (hỏi hành vi đã xảy ra, không dẫn dắt) | Thắng tự phỏng vấn người dùng thật ngoài nhóm và ghi chép nguyên văn | Hà Minh Thắng |
| Viết câu thử (`eval/benchmark.csv`, `metric_spec.yaml`) | Claude, Antigravity (Gemini) | Chuẩn hoá 15 câu `tu_viet` đầu tiên từ các dòng quy định thật của 12 bài Lab ngày K5 (`Day02`–`Day14`) và nháp 4 metric | Cương kiểm lại từng mã `K5-DayXX/FILE#mục` & dòng gốc, bổ sung câu `nguoi_dung`/`data_that` thật trước CP3; Thắng chấm chéo 5 câu | Đặng Đức Cương |
| Sinh data `synthetic` (nếu có) | Không dùng | Không sinh dữ liệu giả lập cho bằng chứng pain | — | — |
| Chấm cột `pass` bằng LLM (nếu có) | Không dùng LLM tự chấm (người chấm + code kiểm metric tất định) | Code kiểm `citation_exists` & `no_solution_leak`, Antigravity trình bày phiếu nguyên văn 30 câu không gợi ý điểm | Hưng/Cương đọc `pass_criterion` chốt tay `1/0` cho 30 câu, Thắng chấm chéo độc lập 5 câu đầu | Đặng Đức Cương, Lê Gia Hưng, Hà Minh Thắng |
| Slide, văn bản (`spec.md`, `slides/`) | Claude, Antigravity (Gemini) | Gợi ý bố cục Mermaid và dàn trang slide từ số liệu có sẵn | Hưng đối chiếu mọi con số trên `spec.md` và slide với file nguồn trong repo | Lê Gia Hưng |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
