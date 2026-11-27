# Dàn slide 8 trang — Nhóm V88 (Track A · Trợ lý đọc tĩnh Codebase & hướng dẫn làm Lab 3 mức sư phạm)

> Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥ 1 con số / trích dẫn có nguồn / kết quả đo truy ngược được về file trong repo.
> Xuất thành `demo-slides.pdf` ở thư mục gốc repo trước **CP4 14:30 Thứ Bảy 28/11**.

| # | Trang | Nội dung cốt lõi của V88 | Số liệu & Trích dẫn lấy từ file | Trạng thái |
|---|---|---|---|---|
| 1 | **Người dùng & Pain** | Học viên L3 (`686` học viên toàn khoá, 3 tuần đầu Phase 1 mỗi ngày 1 lab) phải đối chiếu 3–16 file `.md` (giờ mốc ≠ hạn nộp, 2 file lệch nhau như Day14) để biết nộp gì & làm sao đạt → tốn thời gian, sót yêu cầu, mất điểm lab | • `evidence/lab-checkpoints.csv`: `40` đơn vị lab, K5 trung bình `5,8` CP/lab, `3–16` file `.md`<br>• `evidence/data-mining.md`: `102/453` (`22,5%`) lượt hoàn thành có `skipped=true` (`51,2%` học viên), chỉ `1,11%` chat gắn `lab_key`<br>• `evidence/summary.md`: khảo sát `52` học viên (`80,8%` mất ≥ 15 phút/mốc, `67,3%` từng sót/nhầm) + trích dẫn phỏng vấn `P1..P3` (`CHƯA KIỂM` số ngoài nhóm) | ☐ |
| 2 | **Vì sao chọn bài này (Impact)** | Bảng so sánh 3 hướng: chọn Hướng 1 (đọc tĩnh codebase + dẫn dắt 3 mức sư phạm để người học hiểu *tại sao* & tự làm); loại Hướng 2 (coding agent làm hộ phản sư phạm, Bastani et al. PNAS 2025: `-17%` năng lực tự làm) & loại Hướng 3 (dashboard TA) | • `spec.md` §2 & §3: công thức Impact/tháng (`CHƯA KIỂM` cập nhật từ khảo sát/phỏng vấn thật; ước tính cơ sở `1.200 giờ/tháng`, `2,5 giờ/người gặp/tháng`) | ☐ |
| 3 | **Giải pháp AI & Mức tự động** | Sơ đồ Workflow cố định 4 bước (Read-Only, `0` lệnh shell, `0` sửa file, `1` lần gọi LLM): `scan_lab_codebase` + `search_docs` BM25 → điều phối 3 mức `/1 Giải thích` · `/2 Gợi ý` · `/3 Cầm tay chỉ việc` + gỡ lỗi 3 nhịp → 3 chốt chặn hậu kiểm tất định | • `spec.md` §4 · `codebase/agent.py` · `codebase/tools.py` (4 công cụ Read-Only, nguyên tắc G10/G11/G1-G2/G8-G9) | ☐ |
| 4 | **Demo trực tiếp** | Gắn repo bài lab thực tế (`/repo`), chuyển 3 mức `/1 · /2 · /3`:<br>1) Ca thường/khó: phát hiện xung đột `CODE_LAB.md` 335p vs `CHECKPOINTS.md` 240p ở Day14 (`B08`)<br>2) Ca tấn công: từ chối viết lại hàm lỗi `B18` / tạo JSON giả `B13`, chỉ hướng dẫn nguyên nhân để học viên tự sửa + chạy câu lạ của giám khảo | • `eval/benchmark.csv` (`B08`, `B13`, `B18`) · Link video dự phòng 30s (`CHƯA KIỂM`) | ☐ |
| 5 | **Đánh giá: Lượt 1 → Cải tiến → Lượt 2** | Bộ câu thử `20–30` câu (≥ 1/3 câu thật `nguoi_dung`/`data_that`), 4 metric (`citation_exists`, `requirement_accuracy`, `no_solution_leak`, `honest_when_uncertain`), chuẩn đạt đã khóa ở commit `41ff190` (`≥ 80%` tổng, `100%` `tu_choi`, `100%` mã nguồn hợp lệ); báo cáo trung thực `k/n` Lượt 1 → 1 cải tiến → Lượt 2 | • `eval/README.md` · `eval/report.md` · `eval/run-1.csv` & `eval/run-2.csv` (`CHƯA KIỂM`) · độ khớp chấm chéo `__/5` của Thắng | ☐ |
| 6 | **Chi phí khi dùng thật** | Mô phỏng ≥ 50 phiên trên 3 persona (`deadline_checker` · `in_lab_lookup` · `multi_file_reviewer`), 2 tầng model (`claude-haiku-5-5` \$0.10/\$0.50 & `claude-sonnet-5-5` \$2.00/\$10.00), chi phí / task thành công (chia cho tỉ lệ đạt thật Lượt 2) và 3 kịch bản `300 · 686 · 1.000` học viên so với Impact | • `cost/personas.yaml` · `cost/simulate-1.csv` · `cost/cost-estimate.md` (`CHƯA KIỂM`) | ☐ |
| 7 | **Kết luận (Go / Iterate / Stop)** | Quyết định dựa trên 3 con số thật ở Trang 1 (Pain), Trang 5 (% Đạt vs Chuẩn 80%), Trang 6 (Chi phí/người/tháng vs 2,5 giờ tiết kiệm/người/tháng) + kết quả người dùng thử thật | • Đối chiếu số Trang 1, 5, 6 & `validation/log.md` (`CHƯA KIỂM`) | ☐ |
| 8 | **Nếu có thêm 1 tuần** | (1) Đóng gói VS Code / CLI extension tự nhận diện mốc theo `git status` của bài lab đang mở; (2) Bảng gom câu hỏi vướng lặp nhiều nhất ẩn danh gửi Lab Coach sửa đề gốc; (3) Khắc phục nhóm lỗi còn tồn từ Lượt 2 | • `eval/report.md` mục 4 · `validation/log.md` (`CHƯA KIỂM`) | ☐ |

## Phân công trình bày Demo (mỗi thành viên nắm chắc cả câu chuyện & trình bày phần mình làm)

| Trang | Người trình bày chính | Nội dung Q&A phụ trách sâu |
|---|---|---|
| Trang 1–2 (Pain & Impact) | **Hà Minh Thắng** | Phương pháp đào log `preclass`, khảo sát 52 học viên, phỏng vấn Mom Test & thống kê 40 bài lab |
| Trang 3–4 (Kiến trúc & Live Demo) | **Nguyễn Thế Hoàng** | Cơ chế `scan_lab_codebase` Read-Only, BM25 kéo cặp file lệch nhau, 3 chốt chặn hậu kiểm trong `agent.py` |
| Trang 5–6 (Eval & Mô phỏng chi phí) | **Đặng Đức Cương** | Thiết kế 4 metric, phân tích lỗi Lượt 1 → Lượt 2, công thức chi phí / task thành công |
| Trang 7–8 (Chiến lược sư phạm & Kết luận) | **Lê Gia Hưng** | Triết lý "hiểu tại sao & tự tay làm" vs Coding Agents, quyết định hình dạng Workflow cố định & Go/Iterate |
