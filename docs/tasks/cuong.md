# Nhiệm vụ nhánh `feat/cuong-eval-cost` — Đặng Đức Cương (Eval & Mô phỏng Chi phí)

> **File độc quyền sở hữu trên nhánh này:** `eval/benchmark.csv` *(chỉ nối thêm `B21`–`B30`, cấm xóa/sửa đáp án `B01`–`B20`)*, `eval/run-*.csv`, `traces/*`, `eval/report.md`, `eval/README.md`, `cost/personas.yaml`, `cost/simulate-*.csv`, `cost/cost-estimate.md`, `data/DATA_CARD.md`, `reflection/dang-duc-cuong.md`, `docs/tasks/cuong.md`.
> **TUYỆT ĐỐI KHÔNG SỬA:** `eval/metric_spec.yaml` (ĐÃ KHÓA cứng sau 19:30), `eval/run_eval.py`, `cost/simulate.py`, `spec.md` §7.

## 1. Cấu hình `.env` trên máy (không bao giờ commit `.env`)
```ini
MODEL_PROVIDER=anthropic
MODEL_NAME=claude-haiku-5-5
API_KEY=<key Anthropic của nhóm>
```
*(Lưu ý: khi chạy `eval` và `simulate`, để trống biến `LAB_REPO_PATH` để 100% mã nguồn sinh ra đều thuộc `data/kb_index.json`).*

## 2. Việc cần hoàn thành trước CP3 (09:15 sáng Thứ Bảy 28/11 — hạn nộp Form 2: 10:00)
- [ ] **Mở rộng `eval/benchmark.csv` lên 28–30 câu để đạt ≥ 1/3 câu từ người dùng / data thật:**
  - Hiện đang có `20` câu `tu_viet` (`0/20`). Nếu thêm `10` câu hỏi thật (`B21`–`B30`) với cột `source` bắt đầu bằng `nguoi_dung: ...` (từ khảo sát 52 học viên ở nhánh `feat/thang-evidence` / phỏng vấn `P1..P3`) hoặc `data_that: ...` (từ câu hỏi công khai trên kênh Discord khoá, đã bỏ tên), tỉ lệ sẽ đạt **`10/30` = `33,3%` (≥ 1/3)**!
  - Có thể gắn thử tiền tố `[mode=giai_thich]` hoặc `[mode=cam_tay]` cho 2–3 câu hỏi thật của học viên để kiểm luôn 3 mức hướng dẫn!
  - Chạy `python run.py check` → phải báo **0 dòng `⚠️` ở phần Cần xem lại**!
  - Cập nhật số lượng câu thử mới vào `data/DATA_CARD.md` (Dataset 2) và `eval/README.md` (mục 2).
- [ ] **Chạy Lượt 1 (`eval/run-1.csv`) & Chấm cột `pass`:**
  ```powershell
  python run.py eval
  ```
  - Sẽ sinh ra `eval/run-1.csv` và `traces/run-1.jsonl` (**PHẢI `git add` và commit cả hai file này; tuyệt đối không sửa cột nào ngoài `pass` và `ghi_chu`**).
  - Gửi 5 dòng đầu (`B01`–`B05`, che cột chấm của bạn) cho Thắng chấm độc lập, ghi độ khớp `__/5` vào `eval/README.md` mục 3.
  - Điền `1` hoặc `0` vào cột `pass` cho toàn bộ câu trong `eval/run-1.csv`, sau đó chạy:
    ```powershell
    python run.py score eval/run-1.csv
    ```
- [ ] **Chạy thử mô phỏng chi phí 10 phiên trước CP3:**
  ```powershell
  python run.py simulate --try
  ```

## 3. Việc cần hoàn thành trước CP4 (10:00 → 13:30 Thứ Bảy 28/11 — hạn nộp Form 2: 14:30)
- [ ] Ghi bảng kết quả Lượt 1 + gom nhóm lỗi (≥ 3 lỗi cụ thể `Câu | Input | Output | Vì sao sai`) vào `eval/report.md` mục 1–2.
- [ ] Sau khi Hoàng sửa 1 nhóm lỗi chính và merge vào `main`, bạn `git merge main` vào nhánh này rồi chạy Lượt 2:
  ```powershell
  python run.py eval
  # -> sinh eval/run-2.csv + traces/run-2.jsonl -> chấm cột pass ->
  python run.py score eval/run-2.csv
  ```
- [ ] Hoàn thiện `eval/report.md` mục 3–4 và bảng tổng kết ở `eval/README.md` mục 5–6.
- [ ] **Chạy mô phỏng chi phí chính thức ≥ 50 phiên:**
  ```powershell
  python run.py simulate --rate-from eval/run-2.csv
  ```
  - Commit `cost/simulate-1.csv` + `cost/simulate-1-summary.md` + `traces/simulate-1.jsonl`.
  - Dán bảng kết quả từ `cost/simulate-1-summary.md` vào mục 2 của `cost/cost-estimate.md` (mục 1 đã được điền sẵn khung nguồn từ `cost/personas.yaml`) và viết dòng kết luận so với Impact.

## 4. Trước khóa repo 23:59 Thứ Bảy 28/11
- [ ] Tự viết 3–6 dòng/câu vào `reflection/dang-duc-cuong.md`.
