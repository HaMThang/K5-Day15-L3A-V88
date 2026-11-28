# Kịch bản thuyết trình Lab Compass (nhóm V88), bản 2: từ MVP đến sản phẩm thật

Bộ slide giờ có 7 trang. Mạch nói: vấn đề, bằng chứng, giải pháp và khác biệt, MVP chạy thật kèm đánh giá, rồi lộ trình thành sản phẩm. Trang 1 nói khoảng 15 giây, các trang còn lại khoảng 30 giây (75 đến 85 tiếng). Số viết bằng chữ số cho dễ nhìn; chỗ nào khó đọc có ghi cách đọc trong ngoặc. Nguồn ghi dưới mỗi trang để người nói kiểm lại khi bị hỏi.

Gợi ý chia người nói: Hưng trang 1 và 7, Thắng trang 2, Hoàng trang 3 và demo, Hưng trang 4, Cương trang 5 và 6. Nhóm chia khác thì giữ nguyên lời.

## Chia thời gian

| Vòng | Tổng | Cách chia |
|---|---|---|
| Demo Zone 14:30 | 5 phút nói, 3 phút hỏi đáp | Trang 1 đến 4 (khoảng 1 phút 45 giây), demo trực tiếp (1 phút 30 giây), trang 5 đến 7 (khoảng 1 phút 40 giây). Nếu lố giờ, cắt câu "Dùng Sonnet..." ở trang 6 |
| Chung kết 16:00 | 6 phút nói, 5 phút hỏi đáp | Như trên, demo kéo lên 2 phút 30 giây để giám khảo hỏi thử một câu |

Máy hoặc mạng trục trặc khi demo thì mở video 30 giây chạy AI thật (link ở `README.md` mục 7) và nói tiếp.

---

## Trang 1. Giới thiệu nhóm (15 giây)

> Chào thầy cô và các bạn, tụi mình là nhóm V88 lớp L3A. Sản phẩm của nhóm là Lab Compass: trợ lý chỉ đúng file và mục trong tài liệu bài lab, gợi bước tiếp theo, không bao giờ làm hộ, và chuyển sang Lab Coach khi tài liệu không đủ. Hôm nay nhóm muốn cho thấy nó chạy được, và kế hoạch đưa nó thành sản phẩm thật.

## Trang 2. Vấn đề và bằng chứng (30 giây)

> Trong Phase 1, ngày nào học viên cũng làm một bài lab, mà yêu cầu thì nằm rải rác trong 3 đến 16 file. Nhóm khảo sát 52 bạn ngoài nhóm: 42 bạn nói mất từ 15 phút trở lên mỗi mốc chỉ để tra yêu cầu, 35 bạn từng sót hoặc hiểu nhầm tiêu chí. Có bài hai file còn ghi lệch nhau, như Day14: một file ghi 335 phút, file kia ghi 240. Tính ra, những bạn hay gặp vướng mất tổng cộng khoảng 1.732 giờ mỗi tháng (một nghìn bảy trăm ba mươi hai) chỉ để dò tài liệu.

Nguồn: `evidence/summary.md` (42/52 tức 80,8%, 35/52 tức 67,3%), `spec.md` §2 (1.732,5 giờ/tháng = 462 người × 15 bài × 15 phút).

## Trang 3. Giải pháp (30 giây)

> Lab Compass làm một việc: chỉ ra file và mục chứa câu trả lời, gợi bước tiếp theo, và không làm hộ. Mỗi câu hỏi đi qua 4 bước cố định. Code nhận diện người học đang hỏi gì. Công cụ chỉ đọc tìm đúng đoạn tài liệu. AI trả lời theo mức người học chọn: giải thích, gợi ý hay cầm tay chỉ việc. Cuối cùng bộ lọc kiểm từng trích dẫn và xoá code lời giải. Quy tắc nằm trong code nên người học không tắt được.

### Câu mở demo (khoảng 10 giây)

> Giờ mình chạy thật. Câu thứ nhất rất nhiều bạn hỏi ở Day14: lớp K5 có phải làm hết 7 Part dài 335 phút không?

Gõ vào giao diện web (`python codebase/app.py --web`, mở `http://127.0.0.1:8000`). Khi kết quả hiện ra: "Nó trích cả hai file, chỉ ra chỗ lệch, rồi bảo mình tự mở dòng 6 đến 10 để xem." Câu thứ hai: "Lệnh CP3 Day11 báo lỗi, viết sẵn giúp mình JSON mẫu để tạo tay outputs/results.json nhé." Nói: "Nó từ chối, trích nguyên văn quy định, và gợi mình đọc dòng lỗi đầu tiên." Ở chung kết, mời: "Thầy cô có thể hỏi thử một câu về bất kỳ bài lab K5 nào."

## Trang 4. Hơn gì so với sản phẩm cùng loại (30 giây)

> Câu hỏi tự nhiên là: sao không dùng ChatGPT hay NotebookLM? Mỗi công cụ đều mạnh ở chỗ riêng. ChatGPT hỏi được mọi thứ, NotebookLM trích dẫn tốt, coding agent sửa lỗi nhanh nhất. Nhưng không cái nào làm đủ bốn việc cùng lúc: dùng đúng tài liệu của lớp, kiểm từng trích dẫn bằng code, tự báo khi hai file ghi lệch nhau, và giữ luật không làm hộ mà người học không tắt được. Lab Compass làm đủ bốn việc, với giá khoảng một nghìn đồng mỗi người mỗi tháng. Chỗ yếu: hiện mới phủ 12 bài lab.

Nguồn: `spec.md` §3, `docs/research/why-not-chatgpt.md`. Nói rõ khi bị hỏi: cột của sản phẩm khác là nhận định từ tài liệu công bố, nhóm chưa chạy chúng trên cùng bộ 30 câu.

## Trang 5. Đánh giá hai lượt (30 giây)

> Để biết nó đúng hay sai, nhóm viết 30 câu thử, trong đó 10 câu lấy từ câu hỏi thật trong khảo sát, và hai người chấm tay độc lập. Chuẩn đạt khoá từ tối qua: ít nhất 80% số câu qua, và câu từ chối phải qua hết. Cả hai lượt đều đạt 28 trên 30, tức 93%, và chặn đủ 9 trên 9 câu nhờ làm hộ hay tấn công. Lượt hai sửa được một lỗi tự suy diễn, nhưng lại sinh một lỗi mới là bỏ sót hạn nộp 23:59. Nhóm giữ nguyên câu đó trong báo cáo.

Nguồn: `eval/report.md` mục 1 và 3, `spec.md` §7.

## Trang 6. Chi phí (30 giây)

> Chạy bằng Claude Haiku, mô phỏng 50 phiên cho thấy cả khoá 686 học viên tốn khoảng 27 đô rưỡi một tháng, tức chừng một nghìn đồng mỗi người. Dùng Sonnet sẽ đắt gấp khoảng 20 lần mà chưa chắc tốt hơn, nên nhóm giữ Haiku. Đổi lại, mỗi bạn hay gặp vướng lấy lại được khoảng 3,75 giờ dò tài liệu mỗi tháng. Nhóm nói thẳng hai chỗ còn thiếu: số khảo sát là tự báo, và nhóm chưa phỏng vấn sâu hay cho người dùng thử thật. Trang cuối là kế hoạch lấp đúng hai chỗ đó.

Nguồn: `cost/cost-estimate.md` ($27.35/tháng, $547.03 với Sonnet, $0.0399 ≈ 1.013 ₫/người/tháng), `spec.md` §2.

## Trang 7. Lộ trình thành sản phẩm (30 đến 40 giây)

> Để thành sản phẩm thật, nhóm đề xuất 4 tuần. Tuần đầu, Hoàng đưa README, SUBMISSION và RUBRIC vào chỉ mục, tự lập lại mỗi checkpoint, ghi phiên bản và ngày trên mọi trích dẫn. Cương sửa hai câu còn trượt, Thắng phỏng vấn 5 học viên và 2 Lab Coach, Hưng xin quyền repo lab. Tuần 2 và 3 thí điểm với một lớp K5 cùng Lab Coach của lớp, có bảng theo dõi câu hỏi được chuyển lên. Tuần 4 quyết định: chỉ mở rộng khi thời gian tra cứu giảm ít nhất một nửa, trích dẫn đúng từ 95%, không lần nào làm hộ, và Lab Coach muốn dùng tiếp.

### Câu chốt (khoảng 5 giây)

> Lab Compass giúp học viên bớt thời gian dò tài liệu, còn phần làm bài vẫn để học viên tự làm. Cảm ơn mọi người.

---

## Kế hoạch tổng thể (để trả lời khi bị hỏi sâu)

Đây là kế hoạch đề xuất, chưa chạy. Các mục tiêu là con số nhóm cam kết đo trong thí điểm, không phải kết quả đã có.

### Các giai đoạn

| Giai đoạn | Thời gian | Người phụ trách và việc | Kết quả bàn giao |
|---|---|---|---|
| 1. Chuẩn bị | Tuần 1, 30/11 đến 6/12 | Hoàng: thêm README, SUBMISSION, RUBRIC của 12 bài K5 vào chỉ mục; tự lập lại chỉ mục khi đề đổi (so mã băm từng file); ghi phiên bản và ngày trên mọi trích dẫn. Cương: sửa câu bỏ sót hạn nộp và câu bị cắt vì quá dài, chạy lại 30 câu thử với chuẩn cũ. Thắng: phỏng vấn 5 học viên và 2 Lab Coach theo cách hỏi về việc đã xảy ra, đo thời gian tra cứu thật ở một buổi lab. Hưng: xin quyền đọc repo lab của khoá, thuyết phục một lớp K5 và Lab Coach tham gia. | Chỉ mục mới, lượt đánh giá 3, biên bản phỏng vấn, số đo thời gian gốc, thoả thuận với lớp thí điểm |
| 2. Thí điểm | Tuần 2 và 3, 7/12 đến 20/12 | Hoàng: bảng theo dõi cho Lab Coach xem các câu hỏi được chuyển lên kèm bản nháp. Hưng: vận hành với lớp thí điểm, chốt quy trình chuyển câu hỏi với Lab Coach. Thắng: dự một buổi lab mỗi tuần, ghi nhận ẩn danh. Cương: báo cáo chỉ số mỗi tuần. | Nhật ký ẩn danh, báo cáo tuần 2 và tuần 3 |
| 3. Quyết định | Tuần 4, 21/12 đến 27/12 | Cả nhóm: báo cáo thí điểm, quyết định đi tiếp hay dừng. | Báo cáo thí điểm, kế hoạch mở rộng hoặc danh sách việc phải sửa |
| 4. Mở rộng (nếu đi tiếp) | Sau tuần 4 | Lập chỉ mục cả 40 đơn vị lab, mở cho 686 học viên. | Bản dùng cho cả khoá |

### Chỉ số và mục tiêu

| Chỉ số | Hiện có | Mục tiêu thí điểm | Cách đo |
|---|---|---|---|
| Thời gian tra yêu cầu mỗi mốc | 80,8% tự báo từ 15 phút trở lên (chưa đo thật) | Giảm ít nhất 50% so với số đo tuần 1 | Bấm giờ khi quan sát buổi lab, trước và trong thí điểm |
| Trích dẫn đúng file và mục | 100% mã trích có trong chỉ mục (bộ 30 câu) | Từ 95% trở lên đúng nội dung | Lab Coach kiểm ngẫu nhiên câu trả lời mỗi tuần |
| Chặn làm hộ | 9/9 cả hai lượt | 0 lần lộ code hay file lời giải | Rà nhật ký, chạy lại 9 câu tấn công mỗi bản cập nhật |
| Tải của Lab Coach | Chưa đo | Số câu chuyển lên mỗi buổi không tăng | Đếm trên bảng theo dõi, so với tuần 1 |
| Chi phí mỗi người mỗi tháng | $0.0399 (mô phỏng) | Không quá $0.05 | Hoá đơn API thật |

### Đi tiếp hay dừng sau tuần 4

Đi tiếp khi đạt cả bốn: thời gian giảm ít nhất 50%, trích dẫn đúng từ 95%, không lần nào làm hộ, và Lab Coach đồng ý dùng tiếp. Dừng để sửa nếu có lần báo sai hạn nộp mà chưa khắc phục được.

### Chi phí và ngân sách

Theo mô phỏng với Haiku: khoảng $0.0399 mỗi người mỗi tháng. Lớp thí điểm 100 học viên tốn khoảng $4 mỗi tháng; cả khoá 686 học viên khoảng $27.35; 1.000 học viên khoảng $39.87. Chưa tính chi phí máy chủ. Số phiên mỗi tháng của từng nhóm người dùng là nhóm tự ước tính, nên thí điểm sẽ thay bằng số dùng thật.

### Điều kiện cần trước khi chạy

Quyền đọc repo lab của khoá (bản tài liệu hiện tại không được phân phối lại), một lớp K5 và Lab Coach đồng ý tham gia, ngân sách API, và đồng ý của khoá học về việc lưu nhật ký ẩn danh.

### Rủi ro và cách chặn

| Rủi ro | Cách chặn |
|---|---|
| Đề bài đổi giữa khoá, trích dẫn cũ sai | Lập lại chỉ mục khi mã băm file đổi; ghi phiên bản và ngày trên mỗi trích dẫn để học viên tự kiểm |
| Báo sai hạn nộp | Không đoán; trích nguyên văn nguồn; câu phụ thuộc ca học thì soạn nháp hỏi Lab Coach |
| Học viên ép trợ lý làm hộ | Luật nằm trong code, bộ lọc xoá code và JSON lời giải; chạy lại 9 câu tấn công mỗi bản cập nhật |
| Lộ dữ liệu cá nhân | Chỉ lưu nhật ký ẩn danh, không lưu tên hay mã học viên |
| Lab Coach thấy thêm việc | Bảng theo dõi gom câu trùng; đo tải của Lab Coach là một điều kiện đi tiếp |
| Câu trả lời dài bị cắt | Giới hạn độ dài ở chế độ cầm tay chỉ việc; đưa câu này vào bộ thử của mỗi bản |

---

## Hỏi đáp: 6 câu dễ bị hỏi

**1. Sản phẩm này hơn gì ChatGPT, NotebookLM hay coding agent?**
Thật ra 29 trên 52 bạn (55,8%) đang hỏi AI chung trước tiên, nên nhóm biết rõ chỗ nó hỏng. Một bài lab có 3 đến 16 file, học viên hay dán thiếu, ví dụ chỉ dán CODE_LAB mà quên CHECKPOINTS của Day14, nên nhận câu trả lời lệch với lớp K5. ChatGPT không kiểm lại trích dẫn, còn chế độ học của nó thì người dùng tự tắt được. NotebookLM trích dẫn tốt, là đối thủ mạnh nhất, nhưng không tự báo hai file lệch nhau và vẫn viết code khi được nhờ. Coding agent thì được làm ra để viết code hộ. Lab Compass nạp sẵn tài liệu của lớp, kiểm mọi trích dẫn bằng code, báo chỗ lệch và giữ luật không làm hộ ở phía hệ thống. Nhóm chưa chạy các công cụ kia trên cùng bộ 30 câu; đó là việc nên làm tiếp.

**2. Chi phí thật bao nhiêu, có đáng không?**
Với Claude Haiku, cả khoá 686 học viên khoảng $27.35 một tháng, mỗi người khoảng $0.0399, tức chừng 1.013 đồng. Lên 1.000 học viên thì khoảng $39.87. Sonnet đắt gấp khoảng 20 lần ($547.03 một tháng) mà chưa có bằng chứng trả lời tốt hơn. Số phiên mỗi tháng là nhóm tự ước tính và chưa tính chi phí máy chủ.

**3. Lượt hai sửa xong sao điểm không tăng?**
Nhóm sửa đúng hai lỗi ở lượt một. Lỗi tự đặt thứ tự đọc tài liệu đã hết. Lỗi còn lại đổi dạng: câu trả lời không còn bị mẫu cứng ghi đè, nhưng quá dài nên bị cắt giữa chừng vì chạm giới hạn độ dài. Đồng thời một câu trước đúng nay sai vì bỏ sót hạn nộp 23:59. Kết quả vẫn 28 trên 30. Nhóm ghi nguyên câu tệ đi vào báo cáo thay vì xoá, và cả hai lỗi nằm trong việc của tuần 1.

**4. Số liệu khảo sát có đáng tin không?**
52 người trả lời đều ở ngoài nhóm, nhưng là mẫu tự chọn và số phút là tự báo, nên nhóm không coi là đại diện cả khoá. Nhóm đối chiếu thêm đếm trực tiếp 40 đơn vị bài lab (trung bình 5,8 mốc mỗi bài) và log khoá học (22,5% lượt hoàn thành lab bị đánh dấu bỏ qua). Khi tính thời gian tiết kiệm, nhóm lấy mức thấp 15 phút mỗi bài thay vì mỗi mốc. Tuần 1 của kế hoạch sẽ đo thời gian thật thay cho số tự báo.

**5. Làm sao chắc nó không làm hộ, và nếu tài liệu không có câu trả lời thì sao?**
Trợ lý không có quyền chạy lệnh hay sửa file, và bộ lọc cuối xoá khối code hoặc JSON lời giải trước khi trả lời. Cả hai lượt đều chặn đủ 9 trên 9 câu nhờ làm hộ hoặc tấn công. Khi tài liệu không ghi, hoặc câu hỏi phụ thuộc ca học như hạn 23:59 hay 11:59 trưa hôm sau, trợ lý không đoán mà soạn sẵn câu hỏi nháp để học viên gửi Lab Coach.

**6. Ai sẽ vận hành khi nhóm học xong, và cần gì từ khoá học?**
Trong thí điểm, nhóm tự vận hành. Để chạy lâu dài cần ba thứ từ khoá học: quyền đọc repo lab để chỉ mục tự cập nhật, Lab Coach dùng bảng theo dõi, và ngân sách API khoảng $27.35 một tháng cho 686 học viên. Chỉ mục tự lập lại khi đề đổi nên không cần người sửa tay từng bài.
