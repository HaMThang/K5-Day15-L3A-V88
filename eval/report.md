# Báo cáo đánh giá — Lượt 1 → Một lần cải tiến → Lượt 2

## 1. Kết quả tổng hợp

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-003250` | **28/30** | **93%** | 10/10 (100%) | 9/11 (82%) | 9/9 (100%) | **đạt** (≥ 80% tổng, 100% `tu_choi`, 100% mã nguồn hợp lệ) |
| 2 | *(CP4)* | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

File chi tiết: `eval/run-1.csv`, `eval/run-2.csv`. Nhật ký trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Nhóm lỗi ở Lượt 1

| Nhóm lỗi | Số câu trượt | Câu liên quan |
|---|---|---|
| **Nhóm 1 — Điều kiện `conflict_pair` ghi đè cứng câu trả lời** khi kết quả tìm kiếm kéo kèm cặp mục lệch nhau của Day14, làm mất hướng dẫn theo chế độ người học chọn (`cam_tay` / `giai_thich`) | 1 (`+1` câu giảm chất lượng) | **`B28`** (`pass=0`), `B24` (`pass=1` nhưng mất cách giải thích của `giai_thich`) |
| **Nhóm 2 — Tự suy ra thứ tự đọc tài liệu** từ liên kết giữa các file khi nguồn không quy định thứ tự đọc chính thức | 1 | **`B23`** (`pass=0`) |
| **Nhóm 3 — Regex mã nguồn bắt nhầm ký hiệu `#1` hoặc mã giả** nên chèn cụm `(mục chưa xác thực)` lửng giữa câu | 0 (`2` câu kém tự nhiên) | `B12`, `B20` |

**Ba trường hợp cụ thể từ `eval/run-1.csv`:**

| Câu | Input | Output ở Lượt 1 | Nguyên nhân lỗi |
|---|---|---|---|
| **`B28`** (`pass=0`, `kho`) | `[mode=cam_tay] Mình đang làm Lab Day14, làm sao tự kiểm xem checkpoint nào đã xong 100%, checkpoint nào còn dở?` | `"Phát hiện hai tài liệu trong cùng bài Lab ghi lộ trình khác nhau: 1. Tại [K5-Day14/CHECKPOINTS#lo-trinh-240p]... 2. Tại [K5-Day14/CODE_LAB#lo-trinh-335p]..."` | Học viên hỏi cách tự rà tiến độ từng mốc ở chế độ `cam_tay`, nhưng vì `search_docs` kéo kèm cặp `conflicts_with` của Day14 nên điều kiện `or conflict_pair is not None` trong `codebase/agent.py` ghi đè toàn bộ câu trả lời bằng mẫu báo mâu thuẫn 2 file, làm mất hướng dẫn từng bước `CP0`–`CP8`. |
| **`B23`** (`pass=0`, `kho`) | `Lab Day14 có quá nhiều tài liệu để nắm hết, mình không biết nên đọc tài liệu nào trước?` | `"Theo nguồn, CHECKPOINTS.md là tài liệu định hướng đầu tiên... nên bạn nên đọc CHECKPOINTS.md trước rồi mới đối chiếu CODE_LAB.md."` | Tài liệu chỉ ghi `CHECKPOINTS.md` chứa lộ trình 240 phút của lớp K5 và dẫn link sang 6 file khác (`CHECKPOINTS.md:3`), không quy định thứ tự đọc chính thức; model tự khẳng định `"là tài liệu định hướng đầu tiên"` nên trượt `pass_criterion`. |
| **`B24` & `B12`** (`pass=1`, giảm độ rõ ràng) | `B24`: `[mode=giai_thich] ... Ở Lab Day14 tại sao lớp mình không làm đúng theo giờ trong CODE_LAB.md mà phải xem CHECKPOINTS.md?` · `B12`: hỏi đọc bài mẫu Day02 + mức phạt nộp trễ | `B24`: rơi vào mẫu liệt kê 2 gạch đầu dòng mâu thuẫn thay vì câu giải thích liền mạch · `B12`: xuất hiện chữ `(mục chưa xác thực)` ngay chỗ model viết `#1` | Ở `B24`, tuy vẫn đủ 2 mã nguồn và lý do `"Để vừa 240 phút"` nên đạt tiêu chí chấm, việc ghi đè mẫu cứng làm câu trả lời khô cứng; ở `B12`, biểu thức `_CODE_PATTERN` không bắt buộc dấu `/` trước `#` nên nhận nhầm `#1` là mã mục. |

## 3. Một lần cải tiến (chuẩn bị cho Lượt 2 — CP4)

- **Nhắm vào nhóm lỗi:** Nhóm 1 & Nhóm 2 (xử lý khi truy xuất bài nhiều file như Day14) — **vì sao đáng ưu tiên nhất:** Day14 chính là bài lab nhiều file dễ rối nhất mà học viên cần chế độ `cam_tay` / `giai_thich` và hỏi cách bắt đầu đọc; nếu cứ hỏi tới Day14 lại bị đè bằng thông báo mâu thuẫn chung chung hoặc suy diễn quy tắc ngoài nguồn thì trải nghiệm hướng dẫn 3 mức mất tác dụng.
- **Đã sửa trong `codebase/agent.py`:** (1) Chỉ bật khung báo mâu thuẫn khi `decision == "mau_thuan"`, giữ nguyên câu trả lời theo chế độ `cam_tay`/`giai_thich` ở các câu `tra_cuu`; (2) Ghi rõ trong `SYSTEM` không tự đặt thứ tự đọc tài liệu hay quy chuẩn ngoài nguồn; (3) Siết `_CODE_PATTERN` yêu cầu có `/` trước `#` để không sửa nhầm `#1`.
- **Kết quả sau khi chạy Lượt 2 (`eval/run-2.csv`):** `CHƯA KIỂM` *(chạy và chấm ở CP4)*.
- **Câu nào tệ đi sau khi sửa:** `CHƯA KIỂM`.

## 4. Phần còn lại

- **Giới hạn chưa xử lý:** Chỉ mục mặc định `data/kb_index.json` mới phủ 21 mục của 12 bài Lab ngày K5, chưa có chi tiết từng dòng của mọi file `SUBMISSION.md` và `RUBRIC.md` khi học viên không gắn trực tiếp thư mục lab qua `/repo`.
- **Nếu có thêm 1 tuần:** Mở rộng `data/build_index.py` quét đủ toàn bộ 40 đơn vị bài lab L3 kèm kiểm tra mã băm tự động mỗi khi đề cập nhật, và tổng hợp ẩn danh các mục bị hỏi nhiều nhất trong `traces/` gửi Lab Coach đầu buổi.
