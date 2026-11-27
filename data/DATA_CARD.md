# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Chấm ở rubric R4.

## Dataset 1 · Chỉ mục tài liệu các bài Lab ngày lớp L3 khoá K5 (`data/kb_index.json`)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn tri thức chính thức cho công cụ `search_docs` và `get_section` trong `codebase/tools.py`; căn cứ đối chiếu đáp án `expected` của bộ câu thử |
| **Từ đâu** | Trích xuất có kiểm chứng dòng (`file:dòng`) từ các file `CHECKPOINTS.md` và `CODE_LAB.md` của **12 bài Lab ngày Phase 1 lớp L3 khoá K5** (`Day01` đến `Day14`), tổng hợp tại [evidence/lab-checkpoint-analysis.md](../evidence/lab-checkpoint-analysis.md) và [evidence/lab-checkpoints.csv](../evidence/lab-checkpoints.csv) |
| **Xử lý những bước gì** | (1) Loại bỏ hoàn toàn các bài lab L2 và các kỳ hackathon để chỉ giữ đúng bài lab hàng ngày của L3; (2) Chuẩn hoá mã mục theo `K5-DayXX/<FILE>#<mục>` kèm trường `file` ghi rõ đường dẫn và số dòng gốc; (3) Chỉ lưu bản tóm tắt quy định và 1 câu trích ngắn (≤ 60 từ/mục) để tuân thủ luật không đẩy nguyên văn tài liệu khoá lên repo công khai; (4) Gắn nhãn `conflicts_with` cho cặp file lệch lộ trình (`K5-Day14/CHECKPOINTS#lo-trinh-240p` ↔ `K5-Day14/CODE_LAB#lo-trinh-335p`) qua script `data/build_index.py` |
| **Số dòng / số đoạn** | **21 mục tra cứu (`K5-DayXX/FILE#mục`)** phủ cả 12 bài Lab ngày Phase 1 của K5 (trên nền thống kê 40 đơn vị bài lab L3 ở `evidence/lab-checkpoints.csv`) |
| **Phiên bản / ngày lấy** | `K5-L3-Phase1-Labs` · kiểm đếm ngày `27/11/2026` |
| **Nhãn** | **Thật** (quy định và cấu trúc mốc trích từ tài liệu bài lab thật của khoá, không chứa dữ liệu cá nhân) |
| **Giới hạn** | Bản CP2 mới chỉ mục hoá các mốc trọng tâm của 12 bài Lab ngày Phase 1 K5 (`CHECKPOINTS.md`, `CODE_LAB.md`), chưa nạp chi tiết từng dòng của toàn bộ file `SUBMISSION.md` / `RUBRIC.md` phụ và không chứa thông báo miệng theo ca học của giảng viên / Lab Coach |

## Dataset 2 · Bộ câu thử đánh giá (`eval/benchmark.csv`)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Đo độ chính xác trích dẫn nguồn bài lab, khả năng phát hiện 2 file lab ghi lệch nhau, nhận diện mốc không phải hạn nộp và từ chối viết code/tạo file JSON làm hộ (`eval/run_eval.py` & `cost/simulate.py`) |
| **Từ đâu** | Bản CP2: **15 câu** (`tu_viet`) bám sát các tình huống thực tế trên các bài Lab ngày K5 (`Day02`, `Day04`, `Day06`, `Day09`, `Day11`, `Day12`, `Day13`, `Day14`). Bản CP3: bổ sung lên 24–25 câu, trong đó ≥ 1/3 câu có mã `nguoi_dung` / `data_that` từ phỏng vấn học viên L3 và câu hỏi thật khi làm lab |
| **Xử lý những bước gì** | Ẩn danh tên người hỏi; phân bố trên lưới 4 chiều (bài lab & loại yêu cầu × trạng thái nguồn × hậu quả mất điểm lab × hành vi mong đợi); kiểm định dạng tự động bằng `python run.py check` |
| **Số dòng / số đoạn** | CP2: **15 câu** (`7 thuong · 5 kho · 3 tu_choi`, gồm 2 câu tấn công) |
| **Phiên bản / ngày lấy** | `27/11/2026` |
| **Nhãn** | Hỗn hợp (`tu_viet` ở CP2; bổ sung `nguoi_dung` + `data_that` trước CP3 — không dùng làm bằng chứng pain R1) |
| **Giới hạn** | Ở CP2 câu hỏi được diễn đạt rõ tên ngày lab (trừ câu mơ hồ `B11`); trước CP3 sẽ bổ sung các câu hỏi tự nhiên viết tắt của học viên thật |

## Dataset 3 · Nhật ký hành vi học viên `data/preclass/` & Thống kê 40 bài Lab (dùng cho Bằng chứng Pain R1)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Chứng minh hành vi làm lab (`evidence/data-mining.md`) và độ phân mảnh tài liệu bài lab (`evidence/lab-checkpoint-analysis.md`); không nạp log cá nhân vào `codebase/tools.py` |
| **Từ đâu** | (a) Nhật ký ẩn danh `data/preclass/` do BTC cấp (`05/11–25/11/2026`, lưu gốc tại `data-btc/preclass/` gitignored, đếm bằng `evidence/count_preclass.py`); (b) Bảng kiểm đếm 40 đơn vị bài lab L3 (`evidence/lab-checkpoints.csv`) |
| **Nhãn** | **Thật** |
| **Giới hạn** | Log `preclass` ghi nhận hành vi trên mini-lab trực tuyến (`22,5%` lượt hoàn thành có `skipped=true`, chỉ `1,11%` tin chat gắn `lab_key`), cần kiểm chéo với phỏng vấn trực tiếp học viên L3 về các buổi lab 240 phút nhiều file `.md` |
