# Tóm tắt mô phỏng simulate-1@20261128-093848

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| deadline_checker | 26 | 1 | 5084 | 1123 | 1.0 | 2.8 |
| in_lab_lookup | 17 | 3 | 15647 | 3384 | 3.0 | 7.3 |
| multi_file_reviewer | 7 | 5 | 25321 | 5838 | 5.0 | 11.4 |

Tỉ lệ đạt dùng để tính: 28/30 (93%) — lượt run-2@20261128-081540

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (686 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| claude-haiku-5-5 (vào 0.1 · ra 0.5 $/1M) | $0.0024 (≈ 62 ₫) | $0.0026 (≈ 66 ₫) | $0.0012 (≈ 29 ₫) | $11.96 (≈ 303.816 ₫) | $27.35 (≈ 694.726 ₫) | $39.87 (≈ 1.012.721 ₫) | $0.0399 (≈ 1.013 ₫) |
| claude-sonnet-5-5 (vào 2.0 · ra 10.0 $/1M) | $0.0485 (≈ 1.233 ₫) | $0.0520 (≈ 1.321 ₫) | $0.0232 (≈ 590 ₫) | $239.23 (≈ 6.076.323 ₫) | $547.03 (≈ 13.894.526 ₫) | $797.42 (≈ 20.254.411 ₫) | $0.7974 (≈ 20.254 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.2) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: claude-haiku-5-5. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 25.400 ₫ ((tự ước tính) tỷ giá tham khảo USD/VND tháng 11/2026).
