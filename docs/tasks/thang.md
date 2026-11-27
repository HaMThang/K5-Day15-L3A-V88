# Nhiệm vụ nhánh `feat/thang-evidence` — Hà Minh Thắng (Bằng chứng Pain, Chấm chéo & Người dùng thử)

> **File độc quyền sở hữu trên nhánh này:** `evidence/*` (`summary.md`, `survey/questions.md`, `survey/results.csv`, `interviews/P1.md`..`P3.md`, `data-mining.md`), `validation/log.md`, `reflection/ha-minh-thang.md`, `docs/tasks/thang.md`.
> **Lưu ý quan trọng:** 3 file khảo sát 52 học viên (`evidence/summary.md`, `evidence/survey/questions.md`, `evidence/survey/results.csv`) từ nhánh `hathang` cũ của bạn **đã được tách sạch và nạp sẵn vào nhánh này** (không còn vướng bản cũ `benchmark.csv` 15 câu hay `run-fake.csv`). Hãy làm tiếp trên nhánh `feat/thang-evidence` này, **bỏ nhánh `hathang` cũ**!
> **TUYỆT ĐỐI KHÔNG COMMIT:** file Excel khảo sát gốc còn chứa Họ tên / Email / Mã học viên (vi phạm bị trừ −10 điểm).

## 1. Việc cần hoàn thành trước CP3 (09:00 sáng Thứ Bảy 28/11 — hạn nộp Form 2: 10:00)
- [ ] **Xác nhận thông tin mẫu của bộ khảo sát 52 phản hồi trong `evidence/summary.md` & `evidence/survey/questions.md`:**
  - Đối chiếu trên file gốc ở máy cục bộ của bạn (không commit file gốc!) xem trong 52 người trả lời có **bao nhiêu người ngoài nhóm V88** (chỉ cần ≥ 20 người ngoài nhóm là đạt cứng ngưỡng Đường Khảo sát R1!). Ghi rõ con số `__/52 phản hồi thuộc học viên ngoài nhóm V88`, kênh phát (Discord lớp L3A/L3B...), và khoảng giờ mở/đóng form vào đầu `evidence/summary.md`.
- [ ] **Hoàn thành ≥ 3 biên bản phỏng vấn người thật ngoài nhóm (`evidence/interviews/P1.md`, `P2.md`, `P3.md`):**
  - Ba file khung đã tạo sẵn theo bộ câu hỏi Mom Test của nhóm (tuyệt đối chỉ điền từ cuộc trò chuyện thật với học viên L3 ngoài nhóm / Lab Coach, không ghi tên thật).
  - Cập nhật tóm tắt kết quả `P1..P3` và phần đối chiếu 3 nguồn (*Đào log `preclass` + Phân tích 40 bài lab + Khảo sát 52 người + Phỏng vấn*) vào cuối `evidence/summary.md`.
- [ ] **Chấm chéo mù (Blind Spot-check) 5 output đầu tiên của Lượt 1:**
  - Khi Cương chạy xong `eval/run-1.csv`, nhận 5 dòng đầu (`B01`–`B05`, không nhìn cột chấm của Cương), tự chấm độc lập theo `eval/metric_spec.yaml` rồi gửi kết quả để Cương ghi độ khớp `__/5` (cần ≥ 4/5) vào `eval/README.md`.

## 2. Việc cần hoàn thành cho CP4 (+5 điểm Bonus — trước 13:30 Thứ Bảy 28/11)
- [ ] **Cho ≥ 2 học viên L3 ngoài nhóm dùng thử thật bản MVP (`validation/log.md`):**
  - Mở `python run.py` trên máy có `.env`, giao việc thật theo kết quả (ví dụ: *"Giả sử bạn vừa clone Lab Day14 hoặc Day11, hãy dùng trợ lý ở các mức `/1 · /2 · /3` để kiểm tra xem lớp K5 phải làm những phần nào và khi gặp lỗi ở CP3 thì xử lý sao"*).
  - Điền đủ 5 cột trong `validation/log.md`: *Vai · Việc giao · Quan sát hành vi thật · Trích nguyên văn · Mức nghiêm trọng* + câu hỏi *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* và ≥ 1 rút kinh nghiệm báo cho Hưng ghi vào `spec.md` §10.

## 3. Trước khóa repo 23:59 Thứ Bảy 28/11
- [ ] Tự viết 3–6 dòng/câu vào `reflection/ha-minh-thang.md`.
