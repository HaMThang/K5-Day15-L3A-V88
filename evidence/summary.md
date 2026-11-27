# Tổng hợp bằng chứng: trải nghiệm tra cứu yêu cầu lab

## Nguồn và phạm vi

- **Khảo sát:** file Excel “Khảo sát trải nghiệm tra cứu tài liệu & yêu cầu Lab / Hackathon (AI20K L3)” do nhóm cung cấp, trang dữ liệu đầu tiên, dòng 2–53. Có **52 phản hồi**, cả 52 chọn vai trò “Học viên”; theo xác minh của Thắng, **52/52 người trả lời ở ngoài nhóm V88**. Khảo sát được phát qua Discord, Zalo và trực tiếp. Theo thông tin Thắng cung cấp, form mở 16:00 và đóng 19:10; ngày và múi giờ chưa được ghi nhận. Metadata thời điểm hoàn tất trong bản xuất nằm từ 27/11/2026 14:42 đến 18:53, múi giờ chưa xác nhận; các mốc này chưa khớp rõ với giờ mở/đóng form và cần đối chiếu trước khi chốt.
- Bản đối chiếu đã loại các cột thời gian, email, tên và mã sinh viên: [survey/results.csv](survey/results.csv). Cột `dong_excel` là số dòng trong bảng gốc, giúp tìm lại câu trả lời. File Excel gốc chứa thông tin nhận diện và được giữ cục bộ, không commit.
- Cách tuyển người và thành phần mẫu: theo xác minh của Thắng, toàn bộ **52/52 người trả lời ngoài nhóm V88**; cả 52 tự chọn vai trò “Học viên”. Kênh phát được xác nhận là Discord, Zalo và trực tiếp. Chưa có số người được mời hoặc phân loại lớp L3A/L3B của từng người, nên không xem đây là mẫu đại diện cho toàn khóa. Các tỷ lệ dưới đây chỉ mô tả những người trả lời.
- Các nguồn khác: [đào dữ liệu hành vi](data-mining.md) và [phân tích cấu trúc lab](lab-checkpoint-analysis.md). `P1.md`–`P3.md` hiện là trích xuất phản hồi khảo sát đã chọn ngẫu nhiên, **không phải biên bản phỏng vấn**; chưa có phỏng vấn người dùng ngoài nhóm.

## Kết quả khảo sát

Mẫu số là 52 phản hồi trừ khi ghi khác. Câu hỏi về tài liệu cho phép chọn nhiều đáp án; mỗi người chỉ được đếm một lần cho mỗi loại.

| Câu hỏi | Kết quả |
|---|---|
| Thời gian trung bình tự báo để đọc và tra yêu cầu **mỗi mốc** | Dưới 15 phút: 10/52 (19,2%); 15–30 phút: 29/52 (55,8%); 30–60 phút: 8/52 (15,4%); trên 60 phút: 5/52 (9,6%). Tổng 42/52 (80,8%) chọn từ 15 phút trở lên. Đây là tự báo, không phải thời gian đo thực tế. |
| Đã từng bỏ sót yêu cầu, nộp thiếu **hoặc** hiểu nhầm tiêu chí | Có: 35/52 (67,3%); chưa từng: 10/52 (19,2%); không chắc: 7/52 (13,5%). Câu hỏi gộp ba tình huống, không thể suy ra số người nộp thiếu riêng. |
| Tài liệu thường mở và đối chiếu cùng lúc | README/brief: 50/52; guide: 43/52; rubric: 35/52; luật/quy định: 35/52; file Track: 32/52; thông báo Discord: 20/52. Có 43/52 (82,7%) chọn ít nhất ba loại. Đây là số **loại nguồn được chọn**, không phải số file thực tế. |
| Việc đầu tiên khi phân vân | Hỏi AI chung: 29/52 (55,8%); tự mở lại từng file: 16/52 (30,8%); hỏi thành viên nhóm: 5/52 (9,6%); hỏi Lab Coach/Discord: 2/52 (3,8%). |
| Mức hữu ích của trợ lý được mô tả trong câu hỏi, thang 1–5 | Mức 5: 25/51; mức 4: 18/51; mức 3: 7/51; mức 2: 1/51; mức 1: 0/51. Một người không trả lời. Tổng 43/51 (84,3%) chọn mức 4 hoặc 5. Đây là đánh giá về **ý tưởng được mô tả**, không phải kết quả sử dụng hay kiểm chứng MVP. |

Câu hỏi mở có 35/52 ô không trống, bao gồm cả câu không mô tả trải nghiệm; không coi mọi ô có nội dung là một ví dụ về pain.

## Trích dẫn nguyên văn đã bỏ thông tin nhận diện

Số dòng dưới đây tương ứng `dong_excel` trong bản CSV; trích nguyên văn, không sửa chính tả. Các phát biểu là trải nghiệm tự báo của từng người.

1. “Đôi khi đọc sót những phần bonus hoặc yêu cầu phụ của bài lab, quá nhiều file/thư mục gây rối khi nộp bài sát deadline.” — dòng 5.
2. “Những ngày đầu các yêu cầu chồng chéo giữa các file hướng dẫn làm mình khá rối, ví dụ đặt tên repo phải đọc ở submission, cách làm bài readme, và phải xem cả luật checkpoint rất nhiều yêu cầu không riêng lẻ mà chồng chéo lên nhau” — dòng 18.
3. “Quá nhiều tài liệu để nắm hết và không biết đọc tài liệu nào trước” — dòng 24.
4. “Hôm làm bài lab 9 tôi đã mất rất nhiều thời gian để đọc và tìm kiếm các file cần nộp cũng như check tiêu chí ” — dòng 25.
5. “Đọc GUIDE không hiểu phải mở CHECKPOINT, xong lại check lại RULES xem đã làm đúng chưa rồi mới làm tiếp” — dòng 32.
6. “Ở những buổi học đầu tiên, tôi thấy có quá nhiều file .md với nhiều nội dung khác nhau cần đối chiếu dễ gây rối trong việc đối chiếu kết quả làm bài và tiêu chí nộp” — dòng 33.
7. “Các yêu cầu nộp bài bị chia rải rác ở các file (readme, rubric, rules, submission....)” — dòng 49.
8. “Tôi cứ phải đảo quanh các file rule, submission, guide, readme để tìm kiếm thông tin, các bước tiếp theo, rất là mất thời gian.” — dòng 51.

## Đối chiếu các nguồn và kết luận

- **Khảo sát (tự báo):** 42/52 người (80,8%) cho biết thường mất ít nhất 15 phút tra yêu cầu mỗi mốc; 35/52 (67,3%) từng bỏ sót yêu cầu, nộp thiếu hoặc hiểu nhầm tiêu chí trong câu hỏi gộp; 43/52 (82,7%) chọn ít nhất ba loại tài liệu thường phải đối chiếu. Các trích dẫn ở trên cho thấy một số người mô tả việc phải dò nhiều file, yêu cầu chồng chéo hoặc khó biết nên đọc file nào trước. Theo xác minh của Thắng, cả 52 người trả lời ngoài nhóm V88 và thuộc nhóm người dùng mục tiêu; cả 52 tự chọn vai trò “Học viên”. Chưa có số người được mời và phân loại lớp L3A/L3B, nên chưa kết luận mẫu đại diện toàn khóa.
- **Cấu trúc tài liệu (kiểm đếm):** phân tích 40 đơn vị lab ghi nhận trung bình khoảng 6 checkpoint/lab; lab Phase 1 thường có 5,8 checkpoint và 30–40 phút thiết kế mỗi checkpoint. Các ví dụ trong [phân tích cấu trúc lab](lab-checkpoint-analysis.md) cho thấy một bài có thể dẫn qua nhiều file, có hướng dẫn khác nhau giữa các file hoặc phải phân biệt mốc làm bài với hạn nộp. Nguồn này xác nhận độ phân mảnh trong thiết kế tài liệu, nhưng tự nó không chứng minh học viên đã gặp khó khăn hay mất bao nhiêu thời gian.
- **Nhật ký hành vi (dữ liệu khóa học):** theo [đào dữ liệu hành vi](data-mining.md), 102/453 lượt hoàn thành lab có `skipped=true` (22,5%), 63/123 học viên có log hoàn thành từng bỏ qua ít nhất một lượt (51,2%), và 14/1.260 tin nhắn chat gắn `lab_key` (1,11%). Đây là tín hiệu về hành vi lab và mức sử dụng chat trong ngữ cảnh lab; không chứng minh việc khó tìm yêu cầu là nguyên nhân của việc bỏ qua, cũng không đại diện cho toàn bộ học viên.
- **P1–P3:** các file hiện chứa câu trả lời từ form của ba phản hồi được chọn ngẫu nhiên. Chúng giúp xem một số câu trả lời cá nhân bên cạnh thống kê tổng hợp, nhưng không thay thế phỏng vấn Mom Test. Những chi tiết như sự việc gần nhất, tần suất trong tháng, thời gian xử lý một sự việc cụ thể và phản hồi về trải nghiệm MVP chưa được hỏi.

**Kết luận:** khảo sát và phân tích cấu trúc tài liệu cùng hỗ trợ giả thuyết rằng học viên phải tra cứu nhiều nguồn và có thể bị rối bởi yêu cầu phân tán. Nhật ký hành vi cho biết có lượt bỏ qua lab và ít câu hỏi gắn ngữ cảnh lab, nhưng chưa xác lập quan hệ nhân quả với pain này. Bằng chứng hiện tại chưa đủ để khẳng định mức phổ biến toàn khóa hoặc mức tiết kiệm thời gian của sản phẩm; cần hoàn thành phỏng vấn thật và quan sát người dùng thử MVP.

**Điểm cần xác minh:** Thắng báo form mở 16:00–19:10, nhưng metadata trong bản xuất ghi thời điểm hoàn tất 27/11/2026 14:42–18:53, múi giờ chưa xác nhận. Cần đối chiếu ngày/múi giờ hoặc nguồn giờ trước khi chốt mốc thời gian khảo sát.
