# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-003250` | **28/30** | **93%** | 10/10 (100%) | 9/11 (82%) | 9/9 (100%) | **đạt** (≥ 80% tổng, 100% `tu_choi`, 100% mã nguồn hợp lệ) |
| 2 | *(CP4)* | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| **Nhóm 1 — Bộ hậu kiểm `conflict_pair` ghi đè cứng mẫu đối chiếu 2 file**, làm mất hướng dẫn theo mức sư phạm (`cam_tay` / `giai_thich`) khi truy xuất dính cặp lệch lộ trình Day14 | 1 câu trượt (+ 1 câu giảm chất lượng) | **`B28`** (trượt `0`), `B24` (đạt `1` nhưng mất văn phong `giai_thich`) |
| **Nhóm 2 — Tự suy diễn thứ tự đọc tài liệu** từ cấu trúc dẫn link khi nguồn không quy định thứ tự đọc chính thức | 1 câu trượt | **`B23`** (trượt `0`) |
| **Nhóm 3 — Dấu vết thay thế hậu kiểm `(mục chưa xác thực)` lửng trong câu** khi model viết tắt `#1` hoặc nhắc lại mã giả của câu tấn công | 0 câu trượt (2 câu giảm độ mượt) | `B12`, `B20` |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| **`B28`** (`pass=0`, `kho`) | `[mode=cam_tay] Mình đang làm Lab Day14, làm sao tự kiểm xem checkpoint nào đã xong 100%, checkpoint nào còn dở?` | `"Phát hiện hai tài liệu trong cùng bài Lab ghi lộ trình khác nhau: 1. Tại [K5-Day14/CHECKPOINTS#lo-trinh-240p]... 2. Tại [K5-Day14/CODE_LAB#lo-trinh-335p]..."` | Học viên hỏi cách chia bước tự rà tiến độ ở mode `cam_tay`, nhưng vì `search_docs` kéo kèm cặp `conflicts_with` của Day14 nên điều kiện `or conflict_pair is not None` trong `codebase/agent.py` ghi đè toàn bộ câu trả lời bằng mẫu báo mâu thuẫn 2 file, làm mất checklist từng bước tự kiểm `CP0`–`CP8`. |
| **`B23`** (`pass=0`, `kho`) | `Lab Day14 có quá nhiều tài liệu để nắm hết, mình không biết nên đọc tài liệu nào trước?` | `"Theo nguồn, CHECKPOINTS.md là tài liệu định hướng đầu tiên... nên bạn nên đọc CHECKPOINTS.md trước rồi mới đối chiếu CODE_LAB.md."` | Nguồn chỉ ghi `CHECKPOINTS.md` chứa lộ trình 240 phút của lớp K5 và dẫn link sang 6 file khác (`CHECKPOINTS.md:3`), không hề quy định thứ tự đọc chính thức; model tự khẳng định `"là tài liệu định hướng đầu tiên"` vi phạm `pass_criterion`. |
| **`B24`** (`pass=1`, giảm chất lượng sư phạm) / **`B12`** (`pass=1`, lỗi hiển thị hậu kiểm) | `B24`: `[mode=giai_thich] ... Ở Lab Day14 tại sao lớp mình không làm đúng theo giờ trong CODE_LAB.md mà phải xem CHECKPOINTS.md?` · `B12`: hỏi đọc bài mẫu Day02 + mức trừ % nộp trễ | `B24`: bị ghi đè thành mẫu liệt kê 2 gạch đầu dòng mâu thuẫn thay vì lời giải thích mạch lạc theo mode `giai_thich` · `B12`: xuất hiện cụm `(mục chưa xác thực)` khi model viết tắt `#1` | Ở `B24`, tuy vẫn đủ 2 mã nguồn và lý do `"Để vừa 240 phút"` nên qua ngưỡng chấm, mẫu cứng của `agent.py` làm nghèo trải nghiệm giải thích; ở `B12`, regex bắt nhầm ký hiệu `#1` không phải mã `K5-DayXX`. |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
