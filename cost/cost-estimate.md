# Chi phí khi dùng thật — Nhóm V88

> Số ở mục 2 **không điền tay**: chạy `python run.py simulate --rate-from eval/run-2.csv` → chép nguyên bảng trong `cost/simulate-N-summary.md` sang đây.

## 1. Đầu vào (khớp `cost/personas.yaml`)

- **3 Persona người dùng (`cost/personas.yaml`):**
  1. `deadline_checker` (`50%` người dùng): `12` phiên/tháng × `1` lượt/phiên *(tự ước tính — mở tra nhanh yêu cầu & tiêu chí trước hạn nộp 23:59 hoặc 11:59 trưa hôm sau; cập nhật từ khảo sát/phỏng vấn ở CP3)*.
  2. `in_lab_lookup` (`35%` người dùng): `15` phiên/tháng × `3` lượt/phiên *(tự ước tính — hỏi giải thích/gợi ý các mốc trong buổi lab 240 phút mỗi ngày; cập nhật ở CP3)*.
  3. `multi_file_reviewer` (`15%` người dùng): `20` phiên/tháng × `5` lượt/phiên *(tự ước tính — đối chiếu kỹ nhiều file `.md`/code khung & gỡ lỗi theo mức cầm tay chỉ việc)*.
- **Số người dùng thật (3 kịch bản):**
  - Thấp: **`300`** học viên *(tự ước tính số học viên tra cứu thường xuyên mỗi đợt)*.
  - Cơ sở: **`686`** học viên *(tổng sĩ số toàn khoá trên bảng xếp hạng XP cổng học chụp ngày 27/11: `evidence/sources/leaderboard-686.png`)*.
  - Cao: **`1.000`** học viên *(theo quy mô toàn khoá K5 trong `tracks/track-a-edtech.md`: "hơn 1.000 học viên")*.
- **Giá ≥ 2 tầng mô hình** *(từ `further-reading/model-prices.md` của BTC, tra trang chính thức Anthropic `https://platform.claude.com/docs/en/about-claude/pricing` ngày `25/11/2026`, đơn vị USD / 1M token)*:
  - Tầng Nhỏ (đang chạy thực tế): **`claude-haiku-5-5`** — Vào **\$0.10** · Ra **\$0.50** (prompt ≤ 100K token).
  - Tầng Lớn (đối chiếu nâng cấp): **`claude-sonnet-5-5`** — Vào **\$2.00** · Ra **\$10.00**.
- **Tỉ lệ đạt dùng để tính:** `CHƯA KIỂM` (`__/__ = __%` — lấy từ lượt `eval/run-2.csv` sau khi chấm cột `pass`).
- **Bộ tách token:** Đo token thật trực tiếp trên `claude-haiku-5-5` và tính giá trên cùng họ tokenizer Claude (`claude-haiku-5-5` và `claude-sonnet-5-5`). Tỷ giá quy đổi minh hoạ: `1 USD = 25.400 ₫` *(tự ước tính tháng 11/2026)*.

## 2. Kết quả mô phỏng (`CHƯA KIỂM` — chạy ở CP4)

Lượt mô phỏng: `cost/simulate-__.csv` · run ID `CHƯA KIỂM` · `50` phiên · seed `42`

*(Sau khi chạy `python run.py simulate --rate-from eval/run-2.csv`, dán nguyên bảng từ `cost/simulate-1-summary.md` vào đây)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (300) | / tháng — cơ sở (686) | / tháng — cao (1.000) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `claude-haiku-5-5` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` |
| `claude-sonnet-5-5` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt thật của Lượt 2 — **không coi như đạt 100%**.

## 3. So với Impact (`spec.md` §2)

- **Impact / người gặp / tháng (`spec.md` §2):** Tiết kiệm trung bình ~`150 phút` (`2,5 giờ/người/tháng`, trên quy mô ~`1.200 giờ/tháng` toàn khoá) *(tự ước tính, đối chiếu lại với số khảo sát/phỏng vấn ở CP3)* + giảm rủi ro sót yêu cầu / mất điểm bài lab hàng ngày.
- **Chi phí / người / tháng (kịch bản cơ sở 686 người, `claude-haiku-5-5`):** `CHƯA KIỂM`
- **Kết luận một dòng — đáng làm không:** `CHƯA KIỂM` *(điền sau khi có số đo thật ở mục 2)*.

## 4. Phân tích độ nhạy *(mở rộng)*

- Nhờ kiến trúc **Workflow cố định 4 bước với đúng 1 lần gọi LLM/lượt** (bước quét codebase `scan_lab_codebase` + lọc top-5 đoạn `search_docs` BM25 chạy hoàn toàn bằng Python cục bộ `0 token`), token đầu vào được giữ ổn định quanh ~`4.500–6.000` token thay vì hàng chục nghìn token như coding agent tự lặp nhiều vòng.
- Nếu bật Prompt Caching của Anthropic cho phần `SYSTEM` prompt (`\$0.01 / 1M token` đọc cache trên `claude-haiku-5-5`), chi phí token đầu vào lặp lại giữa các lượt hỏi trong cùng ca lab còn giảm thêm nữa.
