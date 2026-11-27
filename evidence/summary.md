# Tổng hợp bằng chứng: trải nghiệm tra cứu yêu cầu lab

## Nguồn và phạm vi

- **Khảo sát:** file Excel “Khảo sát trải nghiệm tra cứu tài liệu & yêu cầu Lab / Hackathon (AI20K L3)” do nhóm cung cấp, trang dữ liệu đầu tiên, dòng 2–53. Có **52 phản hồi**, cả 52 chọn vai trò “Học viên”. Các thời điểm hoàn tất trong file nằm từ 27/11/2026 14:42 đến 18:53; múi giờ của bản xuất **chưa được xác nhận**.
- Bản đối chiếu đã loại các cột thời gian, email, tên và mã sinh viên: [survey/results.csv](survey/results.csv). Cột `dong_excel` là số dòng trong bảng gốc, giúp tìm lại câu trả lời. File Excel gốc chứa thông tin nhận diện và được giữ cục bộ, không commit.
- Cách tuyển người, kênh phát, số người được mời, danh sách thành viên nhóm và lớp L3A/L3B của từng người: **CHƯA KIỂM**. Vì vậy chưa thể xác nhận đủ ngưỡng **20 người ngoài nhóm, đúng người dùng** theo [mẫu khảo sát](survey/TEMPLATE.md), cũng như chưa thể xem 52 người là mẫu đại diện cho toàn khóa. Các tỷ lệ dưới đây chỉ mô tả những người trả lời.
- Các nguồn khác: [đào dữ liệu hành vi](data-mining.md) và [phân tích cấu trúc lab](lab-checkpoint-analysis.md). Chưa tổng hợp được bằng chứng phỏng vấn người dùng ngoài nhóm.

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

## Đối chiếu và kết luận

Các câu trả lời về nhiều nguồn cần đối chiếu và những trích dẫn trên **phù hợp với giả thuyết** rằng việc tìm yêu cầu rải rác gây khó khăn. Phân tích cấu trúc lab cũng ghi nhận nhiều file hướng dẫn; hai nguồn đo khác nhau: khảo sát là tự báo, còn phân tích lab là kiểm đếm tài liệu. Dữ liệu hành vi về lượt mở, hoàn thành và bỏ qua lab không chứng minh trực tiếp việc khó tìm yêu cầu là nguyên nhân.

Mẫu hiện tại cung cấp tín hiệu cho giả thuyết trong [hypothesis.md](hypothesis.md), nhưng chưa đủ để khẳng định mức phổ biến toàn khóa hoặc mức tiết kiệm thời gian của sản phẩm. Cần xác nhận người trả lời thuộc nhóm người dùng và ngoài đội, kiểm tra cách lấy mẫu, sau đó quan sát người dùng thực sự thử MVP; không suy diễn đánh giá ý tưởng thành kết quả sử dụng.
