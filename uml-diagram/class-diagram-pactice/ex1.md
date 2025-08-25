# Ex1

Một hệ thống quản lý Thư viện (LibMan) của một trường Đại học cho phép quản lý các loại tài
liệu thông thường (sách, giáo trình, tạp chí...). Hệ thống cho phép người quản lý, nhân viên thư
viện và bạn đọc thực hiện các chức năng sau khi đăng nhập:

- Nhân viên quản lí: xem các dạng báo cáo thống kê: các tài liệu theo số lần mượn, các
độc giả theo số lần mượn, các nhà cung cấp theo số lượng tài liệu nhập.
- Nhân viên thư viện: Cập nhật tài liệu, bạn đọc, nhà cung cấp (thêm, xóa, thay đổi), tìm
kiếm, cho mượn tài liệu, nhận trả tài liệu từ bạn đọc, nhập tài liệu từ nhà cung cấp.
- Bạn đọc: mượn tài liệu, trả tài liệu trực tiếp với nhân viên, tìm kiếm thông tin tài liệu,
đăng kí làm thẻ bạn đọc trực tuyến.
- Chức năng bạn đọc tìm thông tin tài liệu: chọn menu tìm tài liệu → nhập tên tài liệu để
tìm → hệ thống hiện danh sách các tài liệu có tên chứa từ khóa vừa nhập → click vào
một tài liệu xem chi tiết → hệ thống hiện thông tin chi tiết về tài liệu.
- Chức năng nhân viên cho bạn đọc mượn tài liệu: chọn menu cho mượn tài liệu → quét
thẻ độc giả (hoặc tìm kiếm theo mã) → Lặp các bước sau cho hết tài liệu mượn: quét mã
tài liệu (hoặc tìm theo mã) → lặp đến khi hết các tài liệu mượn vào thì submit → in
phiếu mượn và giao cho độc giả.

Câu 1 (2 điểm)
- a. Trình bày biểu đồ ca sử dụng (use case) cho hai chức năng: bạn đọc tìm thông tin tài liệu,
và nhân viên cho bạn đọc mượn tài liệu
- b. Trình bày kịch bản (scenario) cho hai ca sử dụng trong Câu 1.a

Câu 2 (2 điểm)
- a. Xác định các lớp thực thể (tên lớp, các thuộc tính cơ bản)
- b. Xây dựng biểu đồ lớp phân tích của các lớp thực thể đã được xác định.

Câu 3 (2 điểm)
- a. Xây dựng biểu đồ giao tiếp (communication diagram) cho hai ca sử dụng trong Câu 1.a.
- b. Xây dựng biểu đồ biểu đồ lớp thiết kế cho hai ca sử dụng trong Câu 1.a.

Câu 4 (2 điểm)
- a. Dựa vào các lớp thực thể, hãy xây dựng các bảng dữ liệu tương ứng với quan hệ lớp có
được.
- b. Dựa vào Câu 3.a, hãy sinh code java (khung lớp, phạm vi thuộc tính/biến, giải thích các
phương thức) từ các lớp có được.

Câu 5 (2 điểm)
- a. Xây dựng biểu đồ biểu đồ gói (package diagram) từ các lớp xác định trong Câu 3.a.
- b. Xây dựng biểu đồ triển khai (deployment diagram) cho kiến trúc ba tầng dựa trên công nghệ
J2EE cho hệ thống.