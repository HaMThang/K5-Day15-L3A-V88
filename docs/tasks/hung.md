# Nhiệm vụ nhánh `feat/hung-spec-slides` — Lê Gia Hưng (Đội trưởng)

> **File độc quyền sở hữu trên nhánh này:** `spec.md` (§0–§6, §8–§10 — **TUYỆT ĐỐI KHÔNG SỬA §7**), `canvas.md`, `README.md`, `slides/*` → `demo-slides.pdf`, `reflection/le-gia-hung.md`, `docs/tasks/hung.md`.

## 1. Việc cần hoàn thành trước CP3 (09:15 sáng Thứ Bảy 28/11 — hạn nộp Form 2: 10:00)
- [ ] **Cập nhật số bằng chứng thật vào `spec.md` §1–§2:** Sau khi Thắng chốt số người ngoài nhóm trên bộ khảo sát 52 phản hồi (`evidence/survey/results.csv` + `evidence/summary.md`) và ≥ 3 phỏng vấn (`P1..P3.md`), thay các chỗ *(tạm ước tính)* ở `spec.md` §1–§2 bằng con số thật có trỏ file nguồn.
- [ ] **Dán link video 30s AI thật (từ Hoàng):** Kiểm tra link mở được ở cửa sổ ẩn danh (Incognito), cập nhật vào mục 7 cuối `README.md` và chuẩn bị điền vào Form 2.
- [ ] **Ghi nhật ký thay đổi `spec.md` §10 (`CP2 → CP4`):** Mọi lần sửa `spec.md` sau 19:30 ngày 27/11 bắt buộc thêm 1 dòng `Thời điểm | Đổi gì | Vì sao`.
- [ ] **Gom nhánh (09:15–09:45) & Nộp Form 2 CP3 (trước 10:00):**
  1. Merge `feat/thang-evidence` → `main`
  2. Merge `feat/hoang-codebase-demo` → `main`
  3. Để Cương merge `main` vào `feat/cuong-eval-cost`, chạy `eval/run-1.csv` + chấm `pass` → merge `feat/cuong-eval-cost` → `main`
  4. Merge `main` vào `feat/hung-spec-slides`, điền số chốt + changelog → merge vào `main` → `python run.py check` → push `main` → nộp Form 2 bằng MSSV `2A202603706`.

## 2. Việc cần hoàn thành trước CP4 (13:45 chiều Thứ Bảy 28/11 — hạn nộp Form 2: 14:30)
- [ ] Điền kết quả Lượt 1 → Lượt 2 (từ `eval/report.md` của Cương) vào `spec.md` §7 dòng *Kết quả* (**chỉ điền dòng Kết quả, tuyệt đối không chạm câu Chuẩn "đạt"**).
- [ ] Điền số mô phỏng chi phí ≥ 50 phiên (từ `cost/cost-estimate.md` của Cương) vào `spec.md` §8.
- [ ] Hoàn thiện 8 trang slide theo `slides/outline.md`, xuất ra file `demo-slides.pdf` đặt ngay thư mục gốc repo.
- [ ] Nộp Form 2 CP4 trước **14:30** và tick đủ **4 Điều kiện cứng xét giải**.

## 3. Trước khóa repo 23:59 Thứ Bảy 28/11
- [ ] Tự viết 3–6 dòng/câu vào `reflection/le-gia-hung.md`.
- [ ] Rà lại bảng `docs/ai-usage.md` và `spec.md` §10 changelog lần cuối.
