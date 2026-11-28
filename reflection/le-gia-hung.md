# Reflection — Lê Gia Hưng (2A202603706)

> Hạn hoàn thành: **23:59 Thứ Bảy 28/11/2026**.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Mình là Đội trưởng nhóm V88, phụ trách định hình bài toán & triết lý sư phạm của sản phẩm, viết và kiểm chứng `spec.md` (§0–§10), `canvas.md`, thiết lập quy chuẩn làm việc đa agent (`AGENTS.md`, `docs/checkpoints-context.md`), dựng bộ slide 8 trang (`slides/slides.html` → `demo-slides.pdf`) và nộp Form 2 cho cả 4 checkpoint.
   - Các mốc đóng góp chính: khởi tạo kiến trúc và chốt khóa chuẩn "đạt" + 20 câu thử CP2 đúng hạn tại commit `41ff190`, đồng bộ tài liệu hậu CP2 kèm nhật ký §10 và tổ chức chia 4 nhánh song song không đụng file (`9eefcb0`, `4cbf830`) để cả nhóm chạy nước rút CP3–CP4.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng Claude và Antigravity (Gemini) để tổng hợp nhanh tài liệu đối chiếu giải pháp tương tự (`docs/research/why-not-chatgpt.md`), vẽ sơ đồ Mermaid ban đầu và kiểm tra chéo tính nhất quán giữa các file trước mỗi mốc nộp.
   - Chỗ quan trọng nhất mình trực tiếp chặn và yêu cầu làm lại: bản nháp đầu của AI thiết kế trợ lý quá thiên về "tra cứu quy chế để nộp không mất điểm"; mình đã định hướng lại mục tiêu cốt lõi là giúp người học **thật sự hiểu *tại sao* bài lab cần bước đó** và refactor toàn bộ `spec.md` §4 sang kiến trúc đọc tĩnh codebase khi học viên fork/clone với 3 mức hướng dẫn (`Giải thích · Gợi ý · Cầm tay chỉ việc`), đồng thời khóa cứng cấm tự sinh dữ liệu, cấm tự setup môi trường và cấm chạy lệnh thay người học.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Ở Lượt 1 (`eval/run-1.csv`, run `run-1@20261128-003250`, đạt `28/30 = 93%`), câu **`B28`** (`[mode=cam_tay]` hỏi cách tự kiểm từng checkpoint đã xong hay còn dở ở Lab Day14) bị trượt (`0` điểm), cùng với câu **`B23`** (tự khẳng định `CHECKPOINTS.md` là tài liệu đọc đầu tiên khi nguồn không quy định thứ tự đọc).
   - Nguyên nhân gốc của `B28` nằm ngay ở thiết kế hậu kiểm quá cứng mà mình đã duyệt: chỉ cần truy xuất Day14 kéo kèm cặp `conflicts_with` (`lo-trinh-240p` vs `lo-trinh-335p`), nhánh `conflict_pair is not None` trong `codebase/agent.py` lập tức ghi đè toàn bộ câu trả lời bằng mẫu báo mâu thuẫn 2 gạch đầu dòng, xóa mất phần hướng dẫn chia bước `cam_tay` mà người học đang thật sự cần. Bài học lớn mình rút ra là guardrail tất định chỉ nên **bổ sung cảnh báo nguồn đối chiếu** khi thiếu, chứ không được ghi đè cứng lên luồng sư phạm của mô hình khi câu hỏi không xoay quanh mâu thuẫn đó.
