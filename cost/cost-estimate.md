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
- **Tỉ lệ đạt dùng để tính chi phí / task thành công:** **28/30 (93%)** từ Lượt 2 `run-2@20261128-081540` (`eval/run-2.csv`, chấm tay, `python run.py simulate --rate-from eval/run-2.csv`).
- **Tỷ giá quy đổi:** `1 USD = 25.400 ₫` *(tự ước tính)*.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-093848` · `50` phiên (0 lỗi) · seed `42` · bảng chép nguyên từ `cost/simulate-1-summary.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| deadline_checker | 26 | 1 | 5084 | 1123 | 1.0 | 2.8 |
| in_lab_lookup | 17 | 3 | 15647 | 3384 | 3.0 | 7.3 |
| multi_file_reviewer | 7 | 5 | 25321 | 5838 | 5.0 | 11.4 |

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (686 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| claude-haiku-5-5 (vào 0.1 · ra 0.5 $/1M) | $0.0024 (≈ 62 ₫) | $0.0026 (≈ 66 ₫) | $0.0012 (≈ 29 ₫) | $11.96 (≈ 303.816 ₫) | $27.35 (≈ 694.726 ₫) | $39.87 (≈ 1.012.721 ₫) | $0.0399 (≈ 1.013 ₫) |
| claude-sonnet-5-5 (vào 2.0 · ra 10.0 $/1M) | $0.0485 (≈ 1.233 ₫) | $0.0520 (≈ 1.321 ₫) | $0.0232 (≈ 590 ₫) | $239.23 (≈ 6.076.323 ₫) | $547.03 (≈ 13.894.526 ₫) | $797.42 (≈ 20.254.411 ₫) | $0.7974 (≈ 20.254 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.2) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: claude-haiku-5-5. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 25.400 ₫ ((tự ước tính) tỷ giá tham khảo USD/VND tháng 11/2026).
- Token đo trên `claude-haiku-5-5`; dòng `claude-sonnet-5-5` tính bằng cùng số token nhân giá Sonnet và dùng tỉ lệ đạt của Haiku (Sonnet chưa chạy eval), nên chỉ là đối chiếu giá.

## 3. Đối chiếu với Impact (`spec.md` §2)

- **Thời gian tiết kiệm ước tính (`spec.md` §2):** Trung bình **`225 phút` (`3,75 giờ/người gặp/tháng`)**, tương đương **`1.732,5 giờ/tháng`** trên ~`462` học viên gặp vướng mắc + giảm rủi ro nộp sót yêu cầu bài lab.
- **Chi phí / người / tháng (cơ sở 686 học viên, `claude-haiku-5-5`):** **\$0.0399 (≈ 1.013 ₫)**; cả khoá ≈ **\$27.35/tháng (≈ 694.726 ₫)**; kịch bản cao 1.000 người ≈ \$39.87/tháng.
- **Kết luận — đáng làm:** với `claude-haiku-5-5`, mỗi học viên tốn khoảng **1.013 ₫/tháng** (≈ \$0.0026 mỗi task thành công) để đổi lấy khoảng 3,75 giờ tra cứu/người gặp/tháng *(tự ước tính, `spec.md` §2)*; chi phí model gần như không đáng kể so với thời gian tiết kiệm. Dùng `claude-sonnet-5-5` đắt hơn khoảng **20 lần** (≈ 20.254 ₫/người/tháng) mà chưa có bằng chứng đạt cao hơn, nên giữ Haiku. Lưu ý: số phiên/tháng của 3 persona là *(tự ước tính)*; mô phỏng chưa tính chi phí hạ tầng, và lỗi `B28` cho thấy câu trả lời dài ở mode `cam_tay` có thể tốn tới 2.048 token ra.

## 4. Ghi chú về cấu trúc chi phí

- Bước quét thư mục `scan_lab_codebase` và lọc top-5 đoạn `search_docs` (BM25) chạy bằng Python cục bộ (`0 token`), mỗi lượt hỏi chỉ gọi mô hình **1 lần** nên lượng token đầu vào giữ ổn định quanh mức ~`4.500–6.000` token thay vì tăng theo nhiều vòng lặp agent.
- Khi triển khai thực tế, có thể bật thêm Prompt Caching của Anthropic cho phần `SYSTEM` prompt (`\$0.01 / 1M token` đọc cache trên `claude-haiku-5-5`) để giảm tiếp chi phí cho các câu hỏi liên tiếp trong cùng buổi lab.
