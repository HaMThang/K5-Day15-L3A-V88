# Ước tính chi phí vận hành thực tế — Nhóm V88

## 1. Tham số đầu vào (`cost/personas.yaml`)

- **Ba nhóm người dùng (persona):**
  1. `deadline_checker` (`50%`): `12` phiên/tháng × `1` lượt/phiên *(tự ước tính — kiểm nhanh yêu cầu nộp bài trước hạn 23:59 hoặc 11:59 trưa hôm sau)*.
  2. `in_lab_lookup` (`35%`): `15` phiên/tháng × `3` lượt/phiên *(tự ước tính — tra cứu các mốc trong buổi lab 240 phút)*.
  3. `multi_file_reviewer` (`15%`): `20` phiên/tháng × `5` lượt/phiên *(tự ước tính — đối chiếu nhiều file `.md`/code khung và hỏi gỡ lỗi)*.
- **Quy mô người dùng (3 kịch bản):**
  - Thấp: **`300`** học viên *(tự ước tính số người dùng thường xuyên mỗi đợt)*.
  - Cơ sở: **`686`** học viên *(sĩ số toàn khoá trên bảng xếp hạng XP cổng học chụp ngày 27/11: `evidence/sources/leaderboard-686.png`)*.
  - Cao: **`1.000`** học viên *(quy mô khoá K5 nêu trong `tracks/track-a-edtech.md`: "hơn 1.000 học viên")*.
- **Đơn giá 2 mô hình cùng họ Claude** *(theo `further-reading/model-prices.md` của BTC, tra ngày `25/11/2026`, đơn vị USD / 1M token)*:
  - Mô hình đang chạy: **`claude-haiku-5-5`** — Vào **\$0.10** · Ra **\$0.50** (prompt ≤ 100K token).
  - Mô hình đối chiếu: **`claude-sonnet-5-5`** — Vào **\$2.00** · Ra **\$10.00**.
- **Tỉ lệ đạt dùng để tính chi phí / task thành công:** `CHƯA KIỂM` *(lấy từ `eval/run-2.csv` khi chạy `python run.py simulate --rate-from eval/run-2.csv` ở CP4)*.
- **Tỷ giá quy đổi:** `1 USD = 25.400 ₫` *(tự ước tính)*.

## 2. Kết quả mô phỏng (`CHƯA KIỂM` — chạy ở CP4)

Lượt mô phỏng: `cost/simulate-__.csv` · run ID `CHƯA KIỂM` · `50` phiên · seed `42`

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (300) | / tháng — cơ sở (686) | / tháng — cao (1.000) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `claude-haiku-5-5` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` |
| `claude-sonnet-5-5` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` | `CHƯA KIỂM` |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt thật của Lượt 2.

## 3. Đối chiếu với Impact (`spec.md` §2)

- **Thời gian tiết kiệm ước tính (`spec.md` §2):** Trung bình **`225 phút` (`3,75 giờ/người gặp/tháng`)**, tương đương **`1.732,5 giờ/tháng`** trên ~`462` học viên gặp vướng mắc + giảm rủi ro nộp sót yêu cầu bài lab.
- **Chi phí / người / tháng (cơ sở 686 học viên, `claude-haiku-5-5`):** `CHƯA KIỂM`
- **Kết luận:** `CHƯA KIỂM` *(chốt sau khi chạy mô phỏng từ Lượt 2)*.

## 4. Ghi chú về cấu trúc chi phí

- Bước quét thư mục `scan_lab_codebase` và lọc top-5 đoạn `search_docs` (BM25) chạy bằng Python cục bộ (`0 token`), mỗi lượt hỏi chỉ gọi mô hình **1 lần** nên lượng token đầu vào giữ ổn định quanh mức ~`4.500–6.000` token thay vì tăng theo nhiều vòng lặp agent.
- Khi triển khai thực tế, có thể bật thêm Prompt Caching của Anthropic cho phần `SYSTEM` prompt (`\$0.01 / 1M token` đọc cache trên `claude-haiku-5-5`) để giảm tiếp chi phí cho các câu hỏi liên tiếp trong cùng buổi lab.
