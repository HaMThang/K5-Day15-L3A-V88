# Data Card — Dữ liệu sử dụng trong bản chạy thử

## Dataset 1 · Chỉ mục tài liệu bài Lab lớp L3 khoá K5 (`data/kb_index.json`)

| Thuộc tính | Chi tiết |
|---|---|
| **Mục đích** | Nguồn dữ liệu cho các công cụ chỉ đọc `scan_lab_codebase`, `search_docs`, `get_section` trong `codebase/tools.py` (kết hợp đọc trực tiếp thư mục lab khi gắn `/repo <path>`) và căn cứ đối chiếu `expected` của bộ câu thử |
| **Nguồn gốc** | Trích xuất có đối chiếu dòng (`file:dòng`) từ `CHECKPOINTS.md` và `CODE_LAB.md` của **12 bài Lab ngày Phase 1 lớp L3 khoá K5** (`Day01`–`Day14`), tổng hợp tại [evidence/lab-checkpoint-analysis.md](../evidence/lab-checkpoint-analysis.md) và [evidence/lab-checkpoints.csv](../evidence/lab-checkpoints.csv) |
| **Các bước xử lý** | (1) Bỏ các bài lab L2 và các kỳ hackathon, chỉ giữ bài lab hàng ngày của L3; (2) Đặt mã chuẩn `K5-DayXX/<FILE>#<mục>` kèm đường dẫn và số dòng gốc; (3) Chỉ giữ tóm tắt và câu trích ngắn ≤ 60 từ/mục kèm mã băm `doc_sha256` (không đưa toàn văn đề lab lên repo công khai); (4) Gắn cờ `conflicts_with` cho cặp file lệch lộ trình ở Day14 qua `data/build_index.py` |
| **Quy mô** | **21 mục**: 20 mục `K5-DayXX/FILE#mục` của **12 bài Lab ngày K5** (`Day01`, `Day02`, `Day04`, `Day06`, `Day07`, `Day08`, `Day09`, `Day10`, `Day11`, `Day12`, `Day13`, `Day14`) + 1 mục quy ước chung `K5-L3-General/QUY-UOC#nhip-lab-va-han-nop`. Chưa có `Day03`, `Day05` (`CHƯA KIỂM`) |
| **Phiên bản** | `K5-L3-Phase1-Labs (2026-11-27)` |
| **Nhãn** | **Thật** (trích từ tài liệu bài lab thật của khoá, không chứa thông tin cá nhân) |
| **Giới hạn** | Mới lập chỉ mục các mục trọng tâm của `CHECKPOINTS.md` và `CODE_LAB.md` ở 12 bài Lab Phase 1 K5; chưa nạp toàn bộ từng dòng của `SUBMISSION.md`, `RUBRIC.md` và không có thông báo riêng theo từng ca học |

## Dataset 2 · Bộ câu thử đánh giá (`eval/benchmark.csv`)

| Thuộc tính | Chi tiết |
|---|---|
| **Mục đích** | Đo độ chính xác khi trích nguồn bài lab, phát hiện hai file ghi lệch nhau, phân biệt giờ mốc với hạn nộp và từ chối làm hộ (`eval/run_eval.py` & `cost/simulate.py`) |
| **Nguồn gốc** | (a) `B01`–`B20` (chốt ở CP2): **20 câu `tu_viet`** dựa trên quy định thật của các bài Lab ngày K5. (b) `B21`–`B30` (bổ sung ở CP3): **10 câu `nguoi_dung`** chuyển từ phản hồi nguyên văn trong khảo sát 52 học viên ([evidence/survey/results.csv](../evidence/survey/results.csv), cột `source` ghi rõ `dong_excel`). Phủ **9/12 bài** trong chỉ mục (`Day02`, `Day04`, `Day06`, `Day09`, `Day10`, `Day11`, `Day12`, `Day13`, `Day14`) |
| **Các bước xử lý** | Bỏ thông tin nhận diện; phân nhóm theo loại bài lab, trạng thái nguồn, hậu quả nếu sai và hành vi mong đợi; kiểm tra tự động bằng `python run.py check` |
| **Quy mô** | **30 câu** (`10 thuong · 11 kho · 9 tu_choi`), gồm 7 câu tấn công `B14`–`B20` và 2 câu kiểm tra chế độ hướng dẫn (`[mode=giai_thich]` ở `B24`, `[mode=cam_tay]` ở `B28`). Tỉ lệ nguồn thật: **10/30** (`≥ 1/3`) |
| **Ngày cập nhật** | `B01`–`B20`: `27/11/2026` · `B21`–`B30`: `28/11/2026` |
| **Nhãn** | Hỗn hợp: `tu_viet` 20 + `nguoi_dung` 10 (chỉ dùng để đánh giá hệ thống, không tính làm bằng chứng pain R1) |
| **Giới hạn** | `B21`–`B30` được viết lại thành câu hỏi từ mô tả vướng mắc trong khảo sát chứ không phải log chat trực tiếp; chưa phủ `Day01`, `Day07`, `Day08` |

## Dataset 3 · Nhật ký hành vi `data/preclass/` & Thống kê 40 bài Lab (dùng cho Bằng chứng Pain R1)

| Thuộc tính | Chi tiết |
|---|---|
| **Mục đích** | Thống kê hành vi làm lab (`evidence/data-mining.md`) và mức độ phân tán tài liệu (`evidence/lab-checkpoint-analysis.md`); không nạp log cá nhân vào `codebase/` |
| **Nguồn gốc** | (a) Bộ log ẩn danh `data/preclass/` do BTC cấp (`05/11–25/11/2026`, lưu cục bộ tại `data-btc/preclass/` git-ignored, đếm bằng `evidence/count_preclass.py`); (b) Bảng kiểm đếm 40 đơn vị bài lab L3 (`evidence/lab-checkpoints.csv`) |
| **Nhãn** | **Thật** |
| **Giới hạn** | Log `preclass` ghi nhận hành vi trên mini-lab trực tuyến (`22,5%` lượt hoàn thành có `skipped=true`, `1,11%` tin chat gắn `lab_key`), không đo trực tiếp số phút học viên đọc file `.md` trên máy nên nhóm đối chiếu thêm với khảo sát 52 học viên L3 |
