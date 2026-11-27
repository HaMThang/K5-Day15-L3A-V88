# Reflection — Lê Gia Hưng (2A202603706)

> Hạn hoàn thành: **23:59 Thứ Bảy 28/11/2026**.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Mình là Đội trưởng nhóm V88, phụ trách định hình bài toán & triết lý sư phạm của sản phẩm, viết và kiểm chứng `spec.md` (§0–§10), `canvas.md`, thiết lập quy chuẩn làm việc đa agent (`AGENTS.md`, `docs/checkpoints-context.md`), dựng bộ slide 8 trang (`slides/slides.html` → `demo-slides.pdf`) và nộp Form 2 cho cả 4 checkpoint.
   - Các mốc đóng góp chính: khởi tạo kiến trúc và chốt khóa chuẩn "đạt" + 20 câu thử CP2 đúng hạn tại commit `41ff190`, đồng bộ tài liệu hậu CP2 kèm nhật ký §10 và tổ chức chia 4 nhánh song song không đụng file (`9eefcb0`, `4cbf830`) để cả nhóm chạy nước rút CP3–CP4.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng Claude và Antigravity (Gemini) để tổng hợp nhanh tài liệu đối chiếu giải pháp tương tự (`docs/research/why-not-chatgpt.md`), vẽ sơ đồ Mermaid ban đầu và kiểm tra chéo tính nhất quán giữa các file trước mỗi mốc nộp.
   - Chỗ quan trọng nhất mình trực tiếp chặn và yêu cầu làm lại: bản nháp đầu của AI thiết kế trợ lý quá thiên về "tra cứu quy chế để nộp không mất điểm"; mình đã định hướng lại mục tiêu cốt lõi là giúp người học **thật sự hiểu *tại sao* bài lab cần bước đó** và refactor toàn bộ `spec.md` §4 sang kiến trúc đọc tĩnh codebase khi học viên fork/clone với 3 mức hướng dẫn (`Giải thích · Gợi ý · Cầm tay chỉ việc`), đồng thời khóa cứng cấm tự sinh dữ liệu, cấm tự setup môi trường và cấm chạy lệnh thay người học.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - *(Cập nhật mã câu `B__` cụ thể ngay sau khi Cương hoàn thành chạy `eval/run-1.csv` trước CP3 sáng 28/11 — tuyệt đối ghi từ kết quả chạy thật, không điền trước khi có `run-1.csv`):* `CHƯA KIỂM — điền từ eval/run-1.csv sáng 28/11`.
