Công Cụ Bẻ Khóa Mật Khẩu Python 
Tài liệu hướng dẫn sử dụng cho công cụ bẻ khóa mật khẩu hai lớp kết hợp giải thuật Hash Modulo tùy chỉnh và SHA-256.
1. Mục đích
Kịch bản Python này được thiết kế để tìm lại mật khẩu bằng phương pháp xác thực hai giai đoạn:
Giai đoạn 1: Băm dữ liệu đầu vào qua hàm custom_hash_modulo.
Giai đoạn 2: Tiếp tục băm kết quả của giai đoạn 1 bằng thuật toán SHA-256 và so sánh với giá trị băm mục tiêu.
Chương trình hỗ trợ hai chế độ dò tìm chính:
Dò tìm theo hồ sơ : Tự động sinh ra các biến thể mật khẩu tiềm năng dựa trên thông tin cá nhân do người dùng cung cấp (tên, ngày sinh, từ khóa liên quan...).
Dò tìm vét cạn : Thử toàn bộ các kết hợp ký tự có thể có theo độ dài mật khẩu được chỉ định.
2. Yêu cầu hệ thống (System Requirements)
Môi trường thực thi: Python 3.x
Thư viện chuẩn : Không cần cài đặt thêm thư viện ngoài, chương trình sử dụng các thư viện có sẵn trong Python:
hashlib,
importlib,
itertools,
os,
re,
string,
sys,
time,
unicodedata.
Tệp phụ thuộc bắt buộc: Phải có tệp hambammodulo.py chứa hàm custom_hash_modulo nằm cùng thư mục làm việc.
3. Hướng dẫn cài đặt và chạy
Cài đặt
Tải hoặc sao chép mã nguồn của tệp thực thi chính và tệp hambammodulo.py.
Đảm bảo máy tính đã cài đặt sẵn Python 3.x.
Chạy chương trình
Đặt tệp mã nguồn chính và tệp hambammodulo.py vào cùng một thư mục.
Mở cửa sổ dòng lệnh  và truy cập đến thư mục chứa tệp.
Chạy lệnh sau để khởi chạy công cụ:
python <ten_tep_tin>.py
Làm theo các hướng dẫn hiển thị trên màn hình:
Chọn chế độ 1 : Nhập các thông tin hồ sơ theo yêu cầu để tạo từ điển mật khẩu tùy chỉnh.
Chọn chế độ 2 : Nhập độ dài mật khẩu cần kiểm tra để bắt đầu quá trình vét cạn.
