# Nhiệm vụ nhánh `feat/hung-spec-slides` — Lê Gia Hưng (Đội trưởng)

> **File độc quyền sở hữu trên nhánh này:** `spec.md` (§0–§6, §8–§10 — **TUYỆT ĐỐI KHÔNG SỬA §7**), `canvas.md`, `README.md`, `slides/*` → `demo-slides.pdf`, `reflection/le-gia-hung.md`, `docs/tasks/hung.md`.

## 1. Các hạng mục ĐÃ HOÀN TẤT trên nhánh `feat/hung-spec-slides`
- [x] **Cập nhật số khảo sát thật 52 phản hồi học viên L3 vào `spec.md` §0–§2 & `canvas.md`:** Đã tích hợp đầy đủ tỉ lệ thật (`80,8%` mất ≥ 15 phút/mốc, `82,7%` mở ≥ 3 loại tài liệu, `67,3%` từng sót/hiểu nhầm, `55,8%` hỏi AI chung đầu tiên), trích dẫn nguyên văn (`results.csv` dòng 32, 51) và công thức Impact có nguồn (`462 × 15 × 15 = 1.732,5 giờ/tháng`, `3,75 giờ/người/tháng`).
- [x] **Đồng bộ bảng giá Claude ở `spec.md` §8 & ghi đầy đủ `spec.md` §10 changelog** (kiểm chứng byte-for-byte **0 thay đổi** ở §7 so với commit khóa `41ff190`).
- [x] **Dựng xong bộ Slide 8 trang chuẩn 16:9 (`slides/slides.html`) + script xuất PDF (`slides/build_pdf.py`) + xuất sẵn bản `demo-slides.pdf`** ở thư mục gốc repo (các ô chờ kết quả `run-1`, `run-2`, `simulate-1` gắn nhãn trung thực `CHƯA KIỂM`).
- [x] **Viết sẵn câu 1 & câu 2 sát thực tế trong `reflection/le-gia-hung.md`** (câu 3 để chờ điền mã câu trượt thật từ `eval/run-1.csv`).

## 2. Việc còn lại khi đồng đội gửi kết quả (Sáng & Trưa Thứ Bảy 28/11)
- [ ] **Trước CP3 (09:15–09:50 sáng 28/11):**
  1. Nhận số xác nhận người ngoài nhóm + tóm tắt phỏng vấn `P1..P3` từ Thắng → cập nhật dòng phỏng vấn ở `spec.md` §1 (+ ghi 1 dòng §10 changelog).
  2. Nhận link video 30s AI thật từ Hoàng → mở thử cửa sổ ẩn danh → dán vào dòng cuối `README.md` mục 7.
  3. Merge theo thứ tự: `feat/thang-evidence` → `feat/hoang-codebase-demo` → `feat/cuong-eval-cost` (đã có `run-1.csv`) → `feat/hung-spec-slides` vào `main` → chạy `python run.py check` → push `main` → bấm nộp **Form 2 CP3 trước 10:00** bằng MSSV `2A202603706`.
- [ ] **Trước CP4 (13:45–14:20 chiều 28/11):**
  1. Điền con số kết quả Lượt 1 → Lượt 2 (từ `eval/report.md`) vào dòng *Kết quả* cuối `spec.md` §7 (**chỉ sửa dòng Kết quả, tuyệt đối không chạm câu Chuẩn "đạt"**) và lên Trang 5 của `slides/slides.html`.
  2. Điền con số từ `cost/simulate-1-summary.md` vào `spec.md` §8 và Trang 6 của `slides/slides.html`, rồi chạy `python slides/build_pdf.py` (2 giây) để cập nhật `demo-slides.pdf`.
  3. Điền nốt câu 3 trong `reflection/le-gia-hung.md` từ 1 câu trượt thật, ghi dòng changelog §10, push `main` và nộp **Form 2 CP4 trước 14:30** (tick đủ 4 Điều kiện cứng xét giải).
