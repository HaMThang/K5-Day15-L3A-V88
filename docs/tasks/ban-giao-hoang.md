# Bàn giao Lab Compass cho nhóm V88

Hoàng bàn giao phần codebase, video demo và các bước phối hợp cho CP3–CP4 ngày 28/11/2026 (UTC+7).

## Hưng · Nộp CP3 trước 10:00

- **[Video nộp CP3 dài 30 giây](https://drive.google.com/file/d/1Y3YC_Mc-mHNwg-iQ-jhyK_tjjcyo7OJC/view).** Ai có link cũng xem được. Đã phát thử khi chưa đăng nhập. Clip cho thấy hai nguồn Day14 và một lần gọi Claude Haiku 5.5 với 5.844 token vào, 1.067 token ra.
- Hoàng xác nhận Hưng đã nhận link trước **09:00**. Hưng dùng link này để nộp Form 2 CP3.
- Nhánh local `feat/hoang-codebase-demo` có các commit `f50ef97` (Web UI), `6799f09` (hash chỉ mục), `00c23c4` (link demo CP3) và `7287516` (reflection). Hoàng push và mở PR vào `main`, rồi nhờ một đồng đội duyệt. [Nhánh GitHub](https://github.com/HaMThang/K5-Day15-L3A-V88/tree/feat/hoang-codebase-demo)

## Cương · Chuẩn bị và chạy lượt 1

1. `python run.py check` hiện báo **0/20** câu từ người dùng hoặc dữ liệu thật. Bổ sung 10 câu có nguồn thật thành B21–B30 để đạt 10/30 theo kế hoạch nhóm. Giữ B01–B20, chuẩn đạt trong `spec.md` §7 và `eval/metric_spec.yaml` theo bản đã khóa.
2. Dùng cùng bộ câu thử và cùng cách chấm cho hai lượt. Bỏ thiết lập `LAB_REPO_PATH` trong môi trường và cấu hình local để chạy trên chỉ mục chuẩn. Cấu hình Anthropic ở máy chạy theo [hướng dẫn nối model](../connect-model.md), giữ API key trong `.env` local.
3. Chạy `python run.py eval --try 3` để kiểm tra kết nối. Kết quả đã có trên máy Hoàng là 3/3 câu có token vào và ra, ghi ở `eval/run-try.csv` và `traces/run-try.jsonl`. Sau đó chạy `python run.py eval`, commit `eval/run-1.csv` và `traces/run-1.jsonl`, điền cột `pass` rồi chạy `python run.py score eval/run-1.csv`.

## Hoàng và Cương · Từ lượt 1 đến CP4

- Khi có kết quả lượt 1 đã chấm, chọn một nhóm lỗi ảnh hưởng nhất và thực hiện đúng một đợt cải tiến trong `codebase/agent.py` hoặc `codebase/tools.py`. Cương chạy lượt 2 sau khi nhận bản cải tiến và dùng hai lượt để cập nhật `eval/report.md` trước CP4 **14:30**.
- Hoàng cập nhật mục 3 của [reflection](../../reflection/nguyen-the-hoang.md) bằng một câu trượt thật, nguyên nhân và kết quả sau cải tiến trước khi khóa repo **23:59**. Hiện mục này ghi lỗi kết nối ở lượt thử.

## Chạy demo và cập nhật chỉ mục

- CLI: `python run.py`. Web: `python codebase/app.py --web` rồi mở `http://127.0.0.1:8000/`. Dùng mức **Gợi ý**, để trống đường dẫn lab và hỏi lớp K5 nên theo lộ trình 335 phút trong `CODE_LAB` hay 240 phút trong `CHECKPOINTS` của Day14.
- Chỉ mục có hash cho 21 mục. Một mục dùng file nguồn và 20 mục dùng bản trích. Khi có đúng bộ tài liệu gốc, chạy `python data/build_index.py --source-root <thư_mục_chứa_Lab>` và kiểm tra `doc_sha256_scope` trong `data/kb_index.json`.
