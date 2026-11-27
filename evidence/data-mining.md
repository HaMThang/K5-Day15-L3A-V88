# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2 · Chấm ở rubric R1.
> Script tái lập có sẵn trong repo: `python evidence/count_preclass.py` (đọc dữ liệu gốc từ `data-btc/preclass/` đã gitignore, người ngoài chạy lại ra đúng 100% các con số dưới đây).

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** Bộ nhật ký hành vi thật đã ẩn danh `data/preclass/events.csv` và danh sách học viên `data/preclass/learners.csv` của khoá AI20K K5 (từ `2026-11-05T04:11:55Z` đến `2026-11-25T09:58:46Z`, tổng cộng `107.709` dòng sự kiện, `721` học viên trong bảng `learners.csv`).
- **Đếm gì & lọc gì:**
  1. Đếm số lượt mở bài lab (`type == "lab_opened"`) và số lượt hoàn thành lab (`type == "lab_completed"`).
  2. Trong các sự kiện `type == "lab_completed"`, giải mã JSON ở cột `data` để đếm số lượt có cờ `"skipped": true` (học viên bấm bỏ qua khi làm lab) và số học viên duy nhất (`hv`) có ít nhất 1 lần `skipped=true`.
  3. Trong các sự kiện gửi tin nhắn hỏi trợ giảng AI (`type == "chat_sent"`), giải mã JSON ở cột `data` để đếm số lượt có trường `lab_key` khác rỗng (hỏi đáp gắn với ngữ cảnh bài lab) so với hỏi ngoài lab.
- **Mẫu số là gì:**
  - Với tỉ lệ lượt hoàn thành lab bị bỏ qua: mẫu số `N = 453` (tổng số sự kiện `lab_completed`).
  - Với tỉ lệ học viên từng bỏ qua bài lab: mẫu số `N = 123` (số mã `hv` duy nhất có ít nhất 1 sự kiện `lab_completed`), đồng thời ghi rõ quy mô `436` học viên có phát sinh log trong `events.csv`.
  - Với tỉ lệ tin nhắn chat gắn với bài lab: mẫu số `N = 1.260` (tổng số sự kiện `chat_sent`).
- **Script chạy kiểm chứng:** `python evidence/count_preclass.py`

## 2. Đọc trước, đếm sau

Đã đọc từ điển cột `column_dictionary.csv` và cấu trúc 13 cột của `events.csv` (`hv, actor, type, lesson_id, kc_code, video, session_id, ref_id, data, catalog_version, learning_mode, occurred_at, received_at`). Hai kiểu hành vi nổi bật quan sát được trước khi tổng hợp:
- Nhiều phiên làm mini-lab kết thúc bằng sự kiện `lab_completed` nhưng trong JSON `data` ghi `"skipped": true` thay vì hoàn thành trọn vẹn yêu cầu.
- Học viên nhắn khá nhiều sự kiện `chat_sent` khi xem bài giảng, nhưng phần lớn `data` không gắn `lab_key` (trợ giảng AI hiện tại phục vụ hỏi bài giảng lý thuyết hơn là tra cứu yêu cầu/vướng mắc lúc làm lab).

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú mẫu số |
|---|---|---|---|
| Học viên có mở bài lab (`lab_opened`) | `147 / 436` | `33,7%` | Trên `436` học viên có sự kiện trong `events.csv` (tổng `602` sự kiện `lab_opened`) |
| Học viên hoàn thành bài lab sau khi mở | `123 / 147` | `83,7%` | Trên `147` học viên đã mở lab (tổng `453` sự kiện `lab_completed`) |
| **Lượt hoàn thành lab nhưng bấm bỏ qua (`skipped=true`)** | **`102 / 453`** | **`22,5%`** | Trên tổng `453` sự kiện `lab_completed` |
| **Học viên từng bấm `skipped=true` ít nhất 1 lần khi làm lab** | **`63 / 123`** | **`51,2%`** | Trên `123` học viên có sự kiện `lab_completed` |
| **Tin nhắn `chat_sent` có gắn ngữ cảnh bài lab (`lab_key`)** | **`14 / 1.260`** | **`1,11%`** | Chỉ `9 / 145` học viên dùng chat từng gửi câu hỏi gắn `lab_key` (`1.246 / 1.260 = 98,89%` không gắn `lab_key`) |

## 4. 5 ví dụ cụ thể từ log (mã `hv` đã ẩn danh bởi BTC, không suy đoán danh tính)

1. `events.csv` dòng `1066`: `type=lab_completed`, `lesson_id=program-day01:ai-llm-foundation`, `lab_key=d01-lab-ban-la-llm`, `skipped=true`, `hv=L0287`, `occurred_at=2026-11-05T18:16:40`
2. `events.csv` dòng `1280`: `type=lab_completed`, `lesson_id=program-day01:ai-llm-foundation`, `lab_key=d01-lab-ban-la-llm`, `skipped=true`, `hv=L0665`, `occurred_at=2026-11-05T23:50:22`
3. `events.csv` dòng `1869`: `type=lab_completed`, `lesson_id=program-day02:ai-problem-definition`, `lab_key=d02-lab-cham-gate`, `skipped=true`, `hv=L0453`, `occurred_at=2026-11-08T01:58:13`
4. `events.csv` dòng `21011`: `type=chat_sent` *(CÓ gắn `lab_key=d04-lab-thu-system-prompt`)*, `hv=L0342`, `occurred_at=2026-11-10T07:32:01`
5. `events.csv` dòng `111`: `type=chat_sent` *(`lab_key` trống — hỏi đáp ngoài ngữ cảnh bài lab)*, `hv=L0213`, `occurred_at=2026-11-05T12:56:39`

## 5. Giới hạn của data

- Nhật ký `data/preclass/` chỉ ghi nhận hành vi trên nền tảng pre-class (mini-lab trực tuyến), **chưa phản ánh hết quá trình làm các bài lab hàng ngày kéo dài 240 phút trên máy tính** (trong 3 tuần đầu học liên tục Phase 1 mỗi ngày đều làm lab, mỗi bài có trung bình `5,8` checkpoint và `3–16` file `.md` hướng dẫn — xem thêm thống kê 40 đơn vị bài lab tại [lab-checkpoint-analysis.md](lab-checkpoint-analysis.md)).
- Dữ liệu cho thấy **hành vi** (`22,5%` lượt hoàn thành lab bị skip trên `51,2%` học viên hoàn thành lab, và `98,89%` lượt chat không gắn với `lab_key`), nhưng không cho biết **vì sao** học viên bỏ qua hoặc mất bao nhiêu phút đối chiếu giữa `CHECKPOINTS.md`, `CODE_LAB.md`, `RUBRIC.md`, `SUBMISSION.md` trước hạn nộp (`23:59` cùng ngày hoặc `11:59` trưa hôm sau với ca `16:00`).
- **Kiểm lại bằng phỏng vấn trực tiếp:** Phỏng vấn ≥ 5 học viên lớp L3 (trong tổng 686 học viên toàn khoá) ngoài nhóm và 1 Lab Coach chiều tối 27/11 theo bộ 5 câu hỏi Mom Test (`evidence/interviews/P1..P5.md`, tổng hợp tại `evidence/summary.md`).
