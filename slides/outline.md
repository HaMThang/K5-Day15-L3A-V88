# Dàn bài 8 trang slide — Nhóm V88 (Lab Compass)

| # | Trang | Nội dung chính | Nguồn đối chiếu trong repo |
|---|---|---|---|
| 1 | **Người dùng & Pain** | Học viên L3 (`686` học viên toàn khoá, 3 tuần Phase 1 mỗi ngày 1 bài lab) phải đối chiếu 3–16 file `.md` (giờ mốc khác hạn nộp, có bài 2 file ghi lệch nhau như Day14) để biết cần nộp gì và thế nào là đạt → mất thời gian tra cứu, dễ sót yêu cầu | `evidence/lab-checkpoints.csv` (`40` đơn vị lab, K5 TB `5,8` CP/bài) · `evidence/data-mining.md` (`22,5%` lượt hoàn thành `skipped=true`, `1,11%` chat gắn `lab_key`) · `evidence/summary.md` (`52/52` phản hồi ngoài nhóm: `80,8%` mất ≥ 15 phút/mốc, `67,3%` từng sót/nhầm) |
| 2 | **Impact & Lý do chọn** | So sánh 3 hướng: chọn Hướng 1 (`~462` HV × `15` bài/tháng × `15` phút = **`1.732,5 giờ/tháng`**, tức `3,75 giờ/người/tháng`); loại Hướng 2 (coding agent làm hộ khiến kết quả tự làm giảm `17%` theo Bastani et al., PNAS 2025) và loại Hướng 3 (dashboard TA) | `spec.md` §2–§3 · `docs/research/why-not-chatgpt.md` |
| 3 | **Thiết kế luồng 4 bước** | Luồng cố định 4 bước chỉ đọc (`0` chạy lệnh, `0` sửa file, `1` lần gọi model): `scan_lab_codebase` + `search_docs` BM25 → trả lời theo 3 mức `/1 Giải thích` · `/2 Gợi ý` · `/3 Cầm tay chỉ việc` → kiểm tra trích dẫn & lọc code/JSON mẫu | `spec.md` §4 · `codebase/agent.py` · `codebase/tools.py` |
| 4 | **Demo thực tế** | Chạy CLI (`python run.py`) và Web (`--web`): (1) Câu `B08` phát hiện 2 file lệch nhau ở Day14 (`CODE_LAB.md` 335p so với `CHECKPOINTS.md` 240p); (2) Câu `B18` / `B13` hướng dẫn gỡ lỗi mà không viết lại hàm hay tạo JSON giả + nhận câu hỏi trực tiếp từ giám khảo | `eval/benchmark.csv` (`B08`, `B13`, `B18`) · Video 30s AI thật tại `README.md` mục 7 |
| 5 | **Đánh giá: Lượt 1 → Lượt 2** | Bộ câu thử `30` câu (`10/30` từ khảo sát thật), 4 metric và chuẩn đạt khóa tại `41ff190`. **Lượt 1 đạt `28/30 (93%)`** (`10/10 · 9/11 · 9/9`), phân tích 2 câu trượt `B28`, `B23` và sửa `agent.py` cho Lượt 2 | `eval/README.md` · `eval/report.md` · `eval/run-1.csv` · `eval/run-2.csv` (`CHƯA KIỂM` ở CP4) |
| 6 | **Chi phí vận hành** | Mô phỏng `50` phiên trên 3 persona, so sánh `claude-haiku-5-5` (\$0.10/\$0.50) và `claude-sonnet-5-5` (\$2.00/\$10.00) ở 3 quy mô `300 · 686 · 1.000` học viên, tính chi phí / task thành công từ tỉ lệ đạt thật | `cost/personas.yaml` · `cost/cost-estimate.md` (`CHƯA KIỂM` ở CP4) |
| 7 | **Kết luận triển khai** | Quyết định thử nghiệm có kiểm soát dựa trên 3 nhóm số liệu: Pain (Trang 1), Chất lượng & Chặn làm hộ 100% (Trang 5), Chi phí so với `3,75 giờ/người/tháng` (Trang 6) + quan sát người dùng thử | `spec.md` §7–§9 · `validation/log.md` |
| 8 | **Hướng phát triển 1 tuần tới** | (1) Quét chỉ mục tự động toàn bộ 40 bài lab kèm kiểm tra mã băm `doc_sha256`; (2) Thêm câu hỏi kiểm tra nhanh sau khi hướng dẫn sửa lỗi; (3) Thống kê ẩn danh các mục học viên hay vướng gửi Lab Coach | `eval/report.md` mục 4 · `TEAMS.md` |

## Phân công trình bày

| Trang | Người trình bày | Phần Q&A phụ trách |
|---|---|---|
| Trang 1–2 | **Hà Minh Thắng** | Đào log `preclass`, khảo sát 52 học viên ngoài nhóm, thống kê 40 bài lab |
| Trang 3–4 | **Nguyễn Thế Hoàng** | Cơ chế quét thư mục chỉ đọc, BM25 kéo cặp file lệch nhau, kiểm tra đầu ra & demo |
| Trang 5–6 | **Đặng Đức Cương** | Bộ 30 câu thử, 4 metric, phân tích lỗi `B28`/`B23` Lượt 1 → Lượt 2 & mô phỏng chi phí |
| Trang 7–8 | **Lê Gia Hưng** | Định hướng "hiểu vì sao & tự làm", kiến trúc luồng 4 bước & kế hoạch triển khai |
