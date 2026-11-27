# Thiết kế bài lab hàng ngày và nhịp checkpoint của khoá AI20K (Lớp L3)

Ngày tổng hợp: `27/11/2026` · Nhóm thực hiện: `V88` (Track A · EdTech).
Bảng số liệu chi tiết của **40 đơn vị bài lab** (không tính hackathon) nằm ở [lab-checkpoints.csv](lab-checkpoints.csv) cùng thư mục `evidence/`. Mỗi dòng đều ghi đường dẫn và số dòng của tài liệu gốc.

## 1. Phạm vi khoá học, nhịp làm lab và cách đếm

- **Quy mô và thời lượng khoá học:** Toàn khoá có tổng cộng **686 học viên** (bảng xếp hạng XP toàn khoá trên cổng học, chụp 27/11: `sources/leaderboard-686.png`; số riêng L3A/L3B CHƯA KIỂM). Lộ trình học tổng thể kéo dài **6 tuần**, trong đó **3 tuần đầu học liên tục Phase 1 (mỗi ngày đều làm bài lab)**, tiếp theo là giai đoạn học chuyên sâu theo các Track.
- **Nhịp nộp bài lab thực tế:** Mỗi ngày học đều có bài lab đi kèm nhiều mốc tự kiểm (checkpoint). Hạn nộp bài lab thường rơi vào **trước 23:59 cùng ngày**, hoặc **11:59 trưa ngày hôm sau** nếu ca học lab diễn ra lúc **16:00 (4h chiều)**.
- **Nguồn tài liệu cấu trúc bài lab đã kiểm đếm:**
  - Phase 1 (Nền tảng L3): các bài lab ngày của K3, K4, K5 (riêng K5 gồm 12 bài lab ngày có bảng checkpoint rõ từ `Day01` đến `Day14`).
  - Sau Phase 1: các bài lab chuyên sâu `Track 1..Track 4`.
  - Không tính các bài lab L2 và loại trừ toàn bộ các kỳ hackathon để chỉ đo đúng bài lab thường nhật của học viên L3.
- **Định nghĩa khi đếm:**
  - *Checkpoint (CP):* mốc được tài liệu gọi tên (`CP`, `Checkpoint`, `Mốc`, `Trạm`, `M0–M5`) và gắn với sản phẩm hoặc lệnh tự kiểm đi kèm. Không tính giờ nghỉ giải lao.
  - *Thời lượng CP:* khoảng thời gian thiết kế từ mốc trước tới mốc hiện tại trong tài liệu; nếu tài liệu không ghi số phút thì để `?`, không tự suy đoán.
  - *Kết quả lọc:* **40 đơn vị bài lab** có bảng checkpoint rõ ràng (`30` bài lab ngày Phase 1 + `10` bài lab Track sau Phase 1).

## 2. Số liệu thống kê cấu trúc bài lab

| Nhóm bài lab | Số đơn vị lab | CP trung bình / lab | Trung vị CP | Min–max CP | Số CP có ghi thời lượng | Thời lượng TB / CP | Trung vị phút / CP | Min–max phút / CP |
|---|---:|---:|---:|---|---:|---:|---:|---|
| **Lab ngày Phase 1 (K3–K5)** | 30 | 5,8 | 5,5 | 3–9 | 161 | 36,7 phút | 35 phút | 10–90 phút |
| **Riêng Lab ngày K5 (Phase 1)** | **12** | **5,8** | **5,5** | **3–9** | **62** | **37,9 phút** | **34 phút** | **10–90 phút** |
| **Lab Track sau Phase 1** | 10 | 6,9 | 6,5 | 5–10 | 54 | 20,9 phút | 20 phút | 5–60 phút |
| **Tổng cộng (Lab ngày + Track)** | **40** | **6,05** | **6** | **3–10** | **215** | **32,7 phút** | **30 phút** | **5–90 phút** |

**Nhận xét chính:**
- Trong 3 tuần đầu học liên tục của Phase 1, mỗi ngày học viên phải đi qua một bài lab dài khoảng 210–240 phút chia thành **trung bình ~6 checkpoint (30–40 phút/mốc)**.
- Sang giai đoạn Track sau Phase 1, thời lượng buổi ngắn hơn (120–150 phút) nhưng số mốc tăng lên **6,9 checkpoint/lab** (~20 phút/mốc), đòi hỏi tra cứu yêu cầu chuyển mốc liên tục.

## 3. Bằng chứng từ cấu trúc tài liệu gây pain "phải mở đối chiếu nhiều file"

1. **Một thư mục bài lab chứa từ 3 đến 16 file `.md` hướng dẫn:** Từ cấu trúc chuẩn L3A/L3B trở đi, bài lab có `CHECKPOINTS.md` thường đi kèm `README.md`, `RUBRIC.md`, `RULES.md`, `SUBMISSION.md`, nhiều bài có thêm `CODE_LAB.md`, `GUIDE.md`/`LAB_GUIDE.md`, `TEAM.md`, `DELIVERY_CHECKLIST.md`. Riêng file `CHECKPOINTS.md` của **K5 Day14** dẫn link tới **6 file khác** (`CODE_LAB.md`, `DAY14_DELIVERY_CHECKLIST.md`, `README.md`, `RUBRIC.md`, `SUBMISSION.md`, `06-lab-complete/README.md`).
2. **Giờ mốc trong `CHECKPOINTS.md` không phải là hạn nộp bài:** Có **5 file `CHECKPOINTS.md`** phải ghi cảnh báo thẳng ở dòng đầu (`K5 Day06:3`, `K5 Day08:3`, `K5 Day13:3`, `K4-L3B Day04:3`, và bản fork Day06). Hạn nộp thực tế nằm ở `SUBMISSION.md` hoặc theo thông báo ca học (trước `23:59` cùng ngày, hoặc `11:59` trưa hôm sau đối với ca lab `16:00` chiều).
3. **Hai file trong cùng một bài lab ghi lộ trình khác nhau:** Tại **K5 Day14** (`CHECKPOINTS.md:6`), tài liệu ghi: *"Lộ trình trong `CODE_LAB.md` dài 335 phút (Part 1–7). Để vừa 240 phút, lớp K5 làm khác ba điểm"*. Học viên chỉ đọc `CODE_LAB.md` mà không đối chiếu `CHECKPOINTS.md` sẽ làm thừa/lệch yêu cầu tại lớp.
4. **Mốc làm tại lớp và mốc làm sau giờ học trộn lẫn:** Ví dụ **K5 Day14** có `CP8` làm sau giờ lab; **K5 Day09** có `M0–M4` làm tại lớp nhưng `M5` làm sau `17:00` với hạn `23:59` (`CHECKPOINTS.md:3-22`); các bài Track 4 (`Day06`, `Day23`) có `CP0` phải hoàn thành ở nhà trước buổi học; **K5 Day12** có `CP0` lồng trong 60 phút của `CP1` và `CP5` lồng trong giờ cuối của `CP4`.
5. **Quy tắc đặt tên vai và điều kiện tính điểm dễ nhầm:** Tại **K5 Day11 Guardrails** (`CHECKPOINTS.md:15-25`), tài liệu phải đóng khung riêng bảng *"Ba agent (nhớ bảng này)"* vì học viên rất dễ lẫn tên vai (`Blue/Red Team`) với tên 3 agent (`Blue`, `Red`, `Red Advance`) và nhầm quy tắc cộng điểm bonus.

*Lưu ý phương pháp luận:* Phân tích cấu trúc tài liệu chứng minh **nguyên nhân thiết kế** khiến học viên phải tra cứu nhiều nơi; nhóm kết hợp thêm nhật ký hành vi `data/preclass/` (`evidence/data-mining.md`) và phỏng vấn trực tiếp học viên L3 ngoài nhóm (`evidence/summary.md`) để xác thực hành vi thực tế.

## 4. Các tình huống tra cứu bài Lab K5 đã xác thực nguồn gốc (dùng cho `data/` và `eval/`)

| # | Bài Lab K5 | Câu hỏi thực tế khi làm lab | Quy định đúng trong tài liệu gốc | Nguồn gốc (`file:dòng`) |
|---|---|---|---|---|
| 1 | K5 Day14 | Kẹt ở một CP quá lâu thì xử lý thế nào? | Quá 10 phút: gọi Lab Coach, ghi lỗi lại, đi tiếp mốc sau | `K5-L3-Day14/CHECKPOINTS.md:25` |
| 2 | K5 Day14 | CP nào nhiều điểm nhất và bao nhiêu điểm? | CP5, chiếm 60/120 điểm | `K5-L3-Day14/CHECKPOINTS.md:25` |
| 3 | K5 Day14 | Có phải làm hết 7 Part (335 phút) trong `CODE_LAB.md` tại lớp không? | Không; `CODE_LAB.md` dài 335 phút nhưng `CHECKPOINTS.md` chốt lớp K5 làm khác 3 điểm để vừa 240 phút (CP8 làm sau giờ) | `K5-L3-Day14/CHECKPOINTS.md:6-10,14-22,114` |
| 4 | K5 Day11 | Có được tự tạo tay file JSON trong `outputs/` không? | Không, file JSON phải được sinh ra khi chạy lệnh thật | `K5-L3-LAB-Day11/CHECKPOINTS.md:5` |
| 5 | K5 Day11 | File nào trong `outputs/` bắt buộc nộp? | `outputs/results.json` và `outputs/attack_results.json` | `K5-L3-LAB-Day11/CHECKPOINTS.md:65,68` |
| 6 | K5 Day11 | Khai thác leak được cả `Red` và `Red Advance` thì có cộng cả hai bonus không? | Không, chỉ tính một phần bonus | `K5-L3-LAB-Day11/CHECKPOINTS.md:23` |
| 7 | K5 Day06 | Bộ benchmark cần bao nhiêu câu và chia tập thế nào? | Tối thiểu ≥ 20 câu, chia 15 dev / 5 test | `K5-L3-Day06/CHECKPOINTS.md:8` |
| 8 | K5 Day06 | Mốc giờ ghi trong `CHECKPOINTS.md` (vd 4:00) có phải hạn nộp bài không? | Không; các mốc chỉ là lịch tích luỹ trong buổi, hạn nộp do giảng viên/coach thông báo | `K5-L3-Day06/CHECKPOINTS.md:3` |
| 9 | K5 Day12 | Video demo dài tối đa bao lâu và nộp ở đâu? | Dưới 5 phút; gắn ở Release `v1.0.0` hoặc lưu `docs/demo/demo.mp4` (< 100 MB), đặt link ở đầu `README.md` | `K5-L3-LAB-Day12/CHECKPOINTS.md:129` |
| 10 | K5 Day09 | Mốc `M5` làm lúc nào và hạn nộp khi nào? | `M0–M4` làm tại lớp; `M5` làm sau 17:00, hạn nộp 23:59 | `K5-Day9/CHECKPOINTS.md:3-22` |
| 11 | K5 Day02 | Không kịp đọc hết bài mẫu trong 15 phút đầu thì ưu tiên đọc phần nào? | Đọc phần nhóm mục 2, 3, 7, 8 | `K5-L3A-Day02/CHECKPOINTS.md:21` |
| 12 | K5 Day13 | Gắn nhãn 20 ca lỗi trong bao lâu, hai người có được trao đổi không? | Làm trong 8 phút, hai người gắn nhãn độc lập, không trao đổi | `K5-L3A-DAY13/CHECKPOINTS.md:26` |

## 5. Giới hạn của bộ thống kê cấu trúc lab
- Thời lượng từng checkpoint là thời lượng **thiết kế** ghi trong tài liệu, không phải thời gian thực tế từng học viên bỏ ra (phần thời gian thực tế tra cứu được đo qua phỏng vấn người dùng ở `evidence/summary.md`).
- Ba đơn vị lab (`K3-K4 Day09`, `K5 Day09`, `Track2 Day18`) có chia mốc nhưng không ghi số phút từng mốc nên chỉ đưa vào thống kê số lượng CP, không tính vào trung bình phút/CP.
