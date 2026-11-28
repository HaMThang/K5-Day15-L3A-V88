# Reflection — Lê Gia Hưng (2A202603706)

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Mình là Đội trưởng nhóm V88, phụ trách chốt bài toán và hướng giải quyết sản phẩm, viết `spec.md` (§0–§10) và `canvas.md`, thiết lập quy tắc làm việc chung (`AGENTS.md`, `docs/checkpoints-context.md`), làm bộ slide 8 trang (`slides/slides.html` → `demo-slides.pdf`) và nộp Form 2 ở các mốc checkpoint.
   - Đóng góp chính theo commit: khóa chuẩn "đạt" và 20 câu thử CP2 đúng hạn tại `41ff190`, chia 4 nhánh làm việc độc lập không đụng file (`9eefcb0`, `4cbf830`), hợp nhất toàn bộ kết quả của 4 thành viên về `main` (lọc bỏ file Excel chứa thông tin cá nhân) và ghi nhận điểm Lượt 1 tại `a0d04b3`.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng Claude và Antigravity (Gemini) để tìm nhanh các bài nghiên cứu đối chiếu giải pháp tương tự (`docs/research/why-not-chatgpt.md`), dựng khung HTML cho slide và rà lại xem số liệu giữa `spec.md`, `eval/`, `evidence/` có bị lệch nhau không.
   - Chỗ lớn nhất mình phải yêu cầu làm lại từ đầu là bản nháp thiết kế đầu tiên của AI quá nghiêng về "hỏi gì đáp nấy để nộp không mất điểm". Mình quyết định đổi lại mục tiêu sang giúp bạn học hiểu **vì sao bài lab cần bước đó**: đọc cấu trúc repo bài lab vừa clone và hướng dẫn theo 3 mức (`Giải thích · Gợi ý · Cầm tay chỉ việc`), đồng thời khóa cứng không viết code hộ, không tự cài môi trường và không chạy lệnh thay người học.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Ở Lượt 1 (`eval/run-1.csv`, run `run-1@20261128-003250`, đạt `28/30 = 93%`), nhóm trượt 2 câu `kho` là **`B28`** (hỏi cách tự kiểm tra tiến độ từng checkpoint ở Day14 với chế độ `cam_tay`) và **`B23`** (tự gọi `CHECKPOINTS.md` là file đọc đầu tiên dù tài liệu không quy định thứ tự đọc).
   - Lỗi ở `B28` đến từ chính nhánh kiểm tra trong `codebase/agent.py` mà mình đã duyệt: cứ hễ câu hỏi đụng tới Day14 khiến công cụ kéo kèm cặp mục `conflicts_with` (`240 phút` so với `335 phút`), code lại ghi đè luôn câu trả lời bằng đoạn thông báo mâu thuẫn 2 file, xóa sạch các bước hướng dẫn `cam_tay` mà người học đang hỏi. Qua câu này mình rút ra là bước kiểm tra bằng code chỉ nên bổ sung dòng lưu ý nguồn đối chiếu khi thiếu, chứ không nên đè cứng lên câu trả lời của mô hình khi người dùng đang hỏi việc khác.
