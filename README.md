# Lab Compass — Trợ lý hướng dẫn làm bài Lab L3 (Nhóm V88)

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md).

**Lát cắt một câu:** Một học viên lớp L3 sau khi clone bài lab về máy · chọn mức hướng dẫn (`Giải thích` / `Gợi ý` / `Cầm tay chỉ việc`) rồi hỏi yêu cầu mốc hoặc dán lỗi đang gặp · trợ lý đọc tài liệu và mã nguồn khung của bài lab để chỉ đúng `file:dòng`, giải thích vì sao cần bước đó, hoặc báo hai file lệch nhau / thiếu nguồn để hỏi Lab Coach · học viên hiểu yêu cầu và tự sửa lỗi, tự chạy lệnh hoàn thành bài.

---

## Chạy nhanh

Yêu cầu **Python 3.10+** (chỉ dùng thư viện chuẩn, không cần `pip install`).

```powershell
copy .env.example .env          # điền MODEL_PROVIDER, MODEL_NAME, API_KEY (xem docs/connect-model.md)
python run.py                   # mở giao diện hỏi đáp CLI
python codebase/app.py --web    # mở giao diện Web tại http://127.0.0.1:8000
python run.py check             # kiểm tra TEAMS.md, benchmark.csv và metric_spec.yaml
```

Trong CLI, gõ `/1` (Giải thích), `/2` (Gợi ý), `/3` (Cầm tay chỉ việc) để đổi mức hướng dẫn, hoặc `/repo <đường_dẫn>` để gắn thư mục bài lab trên máy.

## Các lệnh đánh giá & mô phỏng

| Lệnh | Chức năng |
|---|---|
| `python run.py` | Chạy trợ lý trên CLI, in kèm số lần gọi model, công cụ và token vào/ra |
| `python codebase/app.py --web` | Chạy giao diện Web cục bộ tại `http://127.0.0.1:8000` |
| `python run.py check` | Kiểm tra định dạng `TEAMS.md`, `eval/benchmark.csv` và `eval/metric_spec.yaml` |
| `python run.py eval --fake` | Kiểm tra đường ống đánh giá ở chế độ giả (`eval/run-fake.csv`) |
| `python run.py eval --try` | Chạy thử 3 câu đầu với model thật (`eval/run-try.csv`) |
| `python run.py eval` | Chạy trọn bộ 30 câu thử → `eval/run-N.csv` + `traces/run-N.jsonl` |
| `python run.py score eval/run-1.csv` | Tính tỉ lệ đạt tổng và theo từng loại câu sau khi chấm cột `pass` |
| `python run.py simulate --try` | Chạy thử mô phỏng chi phí 10 phiên (`cost/simulate-try.csv`) |
| `python run.py simulate --rate-from eval/run-2.csv` | Mô phỏng chi phí ≥ 50 phiên theo `cost/personas.yaml` → `cost/simulate-N.csv` |

## Cấu trúc mã nguồn

| File | Vai trò |
|---|---|
| `codebase/app.py` | Giao diện CLI và Web cục bộ (`codebase/web/`) |
| `codebase/agent.py` | `answer(text)` — luồng 4 bước khớp sơ đồ tại `spec.md` §4 |
| `codebase/tools.py` | 4 công cụ chỉ đọc có `@tool`: `scan_lab_codebase`, `search_docs`, `get_section`, `draft_coach_question` |
| `codebase/ai.py` | `call_model(system, user)` — kết nối API model (`anthropic`, `gemini`, `openai`, `ollama`, `fake`) |
| `data/build_index.py` | Tạo chỉ mục `data/kb_index.json` (21 mục quy định có dòng gốc từ 12 bài Lab ngày K5) |

## Phần nào thật, phần nào giả

| Thành phần | Trạng thái | Chi tiết |
|---|---|---|
| Lời gọi mô hình (`codebase/ai.py`) | **Thật** | Gọi `claude-haiku-5-5` qua Anthropic Messages API, lấy `tokens_in`/`tokens_out` trực tiếp từ `usage` |
| Quét thư mục lab & tra cứu BM25 (`codebase/tools.py`) | **Thật (chỉ đọc)** | Đọc các file `.md`/`.py` trong thư mục lab gắn qua `/repo` kết hợp chỉ mục `data/kb_index.json`; tự kéo cặp mục lệch nhau (`conflicts_with`) |
| Kiểm tra trích dẫn & chặn làm hộ (`codebase/agent.py`) | **Thật (bằng code)** | Không cấp công cụ ghi file hay chạy lệnh; chỉ giữ mã nguồn thuộc đoạn vừa đọc; lọc bỏ khối code lời giải hoặc JSON mẫu |
| Hỏi Lab Coach (`draft_coach_question`) | **Bản nháp** | Tạo câu hỏi nháp kèm các mục đã tra để học viên tự xem lại và gửi trên kênh lớp |

## Dùng AI vào việc gì

Nhóm dùng **Claude**, **Codex** và **Antigravity (Gemini)** để tổng hợp tài liệu đối chiếu (`docs/research/`), viết khung tra cứu BM25, giao diện Web, script thống kê log `preclass` và nháp định dạng câu thử. Các thành viên tự kiểm tra lại từng dòng quy định gốc của 12 bài Lab K5, tự khảo sát người học, chốt chuẩn "đạt" (`spec.md` §7) và chấm tay kết quả đánh giá. Xem chi tiết tại [docs/ai-usage.md](docs/ai-usage.md).

## Bảy hạng mục nộp bài

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp tại [evidence/summary.md](evidence/summary.md)) |
| 2 | Impact có số | [spec.md](spec.md) §2 |
| 3 | Thiết kế giải pháp | [spec.md](spec.md) §4 |
| 4 | Bản chạy thử | `codebase/` (`python run.py`) |
| 5 | Định nghĩa "tốt" + bộ câu thử | [data/DATA_CARD.md](data/DATA_CARD.md) · `eval/` ([eval/README.md](eval/README.md), [eval/report.md](eval/report.md)) |
| 6 | Mô phỏng chi phí | `cost/` ([cost/personas.yaml](cost/personas.yaml), [cost/cost-estimate.md](cost/cost-estimate.md)) |
| 7 | Slide + demo + video dự phòng | [demo-slides.pdf](demo-slides.pdf) ([slides/slides.html](slides/slides.html)) · [Video 30s AI thật (CP3)](https://drive.google.com/file/d/1Y3YC_Mc-mHNwg-iQ-jhyK_tjjcyo7OJC/view) |
| + | Người dùng thử *(bonus)* | [validation/log.md](validation/log.md) |
