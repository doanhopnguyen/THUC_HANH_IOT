#Chuẩn bị môi trường cho Bài 1 và Bài 2
    Python đã dùng để chạy thử: 3.11.9
    Thư viện đã dùng: paho-mqtt 2.1.0 (hỗ trợ CallbackAPIVersion.VERSION2)
    Mở PowerShell tại thư mục gốc THUC_HANH_IOT.
    Tạo môi trường và cài thư viện (chỉ cần làm lần đầu):
        python -m venv .venv
        .\.venv\Scripts\python.exe -m pip install paho-mqtt==2.1.0
    Nếu đã có .venv và thư viện thì bỏ qua bước cài đặt.
    Các lệnh bên dưới chạy từ thư mục gốc, không cần kích hoạt .venv.

_______BAI1_________
#Mục đích
    Gửi lời chào từ publisher và nhận thông điệp bằng subscriber qua MQTT.
    File gửi: Bai1/publisher_bai1.py
    File nhận: Bai1/subscriber_bai1.py

#Broker sử dụng
    Dùng broker công khai của EMQX.
        Địa chỉ: broker.emqx.io
        Cổng: 1883 (MQTT TCP, không dùng TLS)
        Tài khoản: không cấu hình username/password trong chương trình
        Topic: iot/lab/message
    Publisher gửi thông điệp đến broker; broker chuyển tiếp đến subscriber
    đã đăng ký cùng topic.

#Cách chạy
    # Terminal 1 - chạy subscriber trước
        .\.venv\Scripts\python.exe -u .\Bai1\subscriber_bai1.py
    Đợi xuất hiện: Dang lang nghe topic: iot/lab/message

    # Terminal 2 - chạy publisher
        .\.venv\Scripts\python.exe -u .\Bai1\publisher_bai1.py
    Publisher gửi một thông điệp rồi tự kết thúc.
    Subscriber tiếp tục lắng nghe; nhấn Ctrl+C để dừng.

#Kết quả chạy thực tế (08/10/2026)
    Terminal 2 - publisher:
        Da gui message:
        Xin chao tu client Python MQTT - B23DCC350 - Nguyen Doan Hop

    Terminal 1 - subscriber:
        Ket noi MQTT broker thanh cong
        Dang lang nghe topic: iot/lab/message

        Nhan duoc message:
        Topic: iot/lab/message
        Payload: Xin chao tu client Python MQTT - B23DCC350 - Nguyen Doan Hop
        Time: 14:38:52

    Kết quả: publisher gửi thành công, subscriber nhận đúng topic và payload.
    Time là giờ trên máy chạy subscriber lúc nhận thông điệp và sẽ thay đổi
    ở những lần chạy khác.

_______BAI2_________
#Mục đích
    Mô phỏng cảm biến sensor01 gửi dữ liệu nhiệt độ và độ ẩm dạng JSON.
    File gửi: Bai2/sensor_publisher_bai2.py
    File nhận và cảnh báo: Bai2/monitor_subscriber_bai2.py

#Broker sử dụng
    Dùng broker công khai của EMQX.
        Địa chỉ: broker.emqx.io
        Cổng: 1883 (MQTT TCP, không dùng TLS)
        Tài khoản: không cấu hình username/password trong chương trình
        Topic: iot/lab/sensor01/data

#Dữ liệu và điều kiện cảnh báo
    Publisher tạo ngẫu nhiên dữ liệu mỗi 3 giây:
        device_id: sensor01
        temperature: từ 25 đến 40 độ C, làm tròn 1 chữ số thập phân
        humidity: từ 30 đến 80 %, làm tròn 1 chữ số thập phân
    Monitor đọc JSON và hiển thị thiết bị, nhiệt độ, độ ẩm.
        temperature > 35: CANH BAO: Nhiet do cao
        humidity < 40: CANH BAO: Do am thap
    Hai điều kiện được kiểm tra riêng; có thể xuất hiện cả hai cảnh báo.
    Nhiệt độ bằng 35 hoặc độ ẩm bằng 40 không kích hoạt cảnh báo tương ứng.

#Cách chạy
    # Terminal 1 - chạy monitor trước
        .\.venv\Scripts\python.exe -u .\Bai2\monitor_subscriber_bai2.py
    Đợi xuất hiện: Dang lang nghe topic: iot/lab/sensor01/data

    # Terminal 2 - chạy sensor publisher
        .\.venv\Scripts\python.exe -u .\Bai2\sensor_publisher_bai2.py
    Hai chương trình chạy liên tục. Nhấn Ctrl+C ở mỗi terminal để dừng.

#Kết quả chạy thực tế (08/10/2026, trích các mẫu đã gửi và nhận)
    Terminal 1 - monitor khi kết nối:
        Ket noi MQTT broker thanh cong
        Dang lang nghe topic: iot/lab/sensor01/data

    Mẫu 1 - dữ liệu bình thường:
        Terminal 2:
            Da gui:
            {"device_id": "sensor01", "temperature": 34.6, "humidity": 69.4}
        Terminal 1:
            ------------------------
            Device: sensor01
            Temperature: 34.6 C
            Humidity: 69.4 %

    Mẫu 2 - độ ẩm thấp:
        Terminal 2:
            Da gui:
            {"device_id": "sensor01", "temperature": 32.9, "humidity": 30.9}
        Terminal 1:
            ------------------------
            Device: sensor01
            Temperature: 32.9 C
            Humidity: 30.9 %
            CANH BAO: Do am thap

    Mẫu 3 - nhiệt độ cao:
        Terminal 2:
            Da gui:
            {"device_id": "sensor01", "temperature": 36.5, "humidity": 45.4}
        Terminal 1:
            ------------------------
            Device: sensor01
            Temperature: 36.5 C
            Humidity: 45.4 %
            CANH BAO: Nhiet do cao

    Kết quả: monitor nhận đúng dữ liệu JSON do sensor publisher gửi;
    đã quan sát được cả cảnh báo nhiệt độ cao và cảnh báo độ ẩm thấp.
    Các giá trị được tạo ngẫu nhiên nên sẽ khác ở những lần chạy khác.

_______BAI3_________
#Broker sử dụng
    Dùng Broker công khai của EMQX
        Địa chỉ: broker.emqx.io
        Cổng: 1883 (đây là cổng MQTT chuẩn, k cần mã hoá TLS)
        Tài khoản: k cần, ai cx kết nối đc
    Broker là máy chủ trung gian. Thiết bị và controller không kết nối trực tiếp với nhau, cả 2 chỉ kết nối qua broker

#Cách chạy
    # Terminal 1
    python device_bai3.py

    # Terminal 2
    python controller_bai3.py
    Thiet bi: light01, fan01, pump01
    Cu phap: ON | OFF | <thiet bi> ON | <thiet bi> OFF | EXIT
    Nhap lenh:                                          // Nhập cú pháp lệnh để bật, tắt thiết bị

#Kết quả
Terminal 1                                |                  Terminal 2
python device_bai3.py                     |       python controller_bai3.py
Ket noi MQTT broker thanh cong            |       Thiet bi: light01, fan01, pump01
Da gui trang thai:                        |       Nhap lenh:
{"device_id": "light01", "status": "OFF"} |
Dang lang nghe topic: iot/lab/fan01/cmd   |
Da gui trang thai:                        |
{"device_id": "fan01", "status": "OFF"}   |
Dang lang nghe topic: iot/lab/pump01/cmd  |
Da gui trang thai:                        |
{"device_id": "pump01", "status": "OFF"}  |       
----------------------------------------
Thiet bi: light01                         |         Nhap lenh: ON
Nhan duoc lenh: ON                        |         Da gui lenh ON toi light01
light01 da BAT                            |         Nhap lenh:
Da gui trang thai:                        |         Trang thai nhan duoc:
{"device_id": "light01", "status": "ON"}  |         {"device_id": "light01", "status": "ON"}     
     
-----------------------------------------
Thiet bi: fan01                           |         Nhap lenh: fan01 ON
Nhan duoc lenh: ON                        |         Da gui lenh ON toi fan01
fan01 da BAT                              |         Nhap lenh:
Da gui trang thai:                        |         Trang thai nhan duoc:
{"device_id": "fan01", "status": "ON"}    |         {"device_id": "fan01", "status": "ON"}     

------------------------------------------
                                          |         Nhap lenh: tv01 ON
                                          |         Loi: khong co thiet bi tv01
                                          |         Nhap lenh:
      
------------------------------------------
Thiet bi: light01                         |         Nhap lenh: OFF
Nhan duoc lenh: OFF                       |         Da gui lenh OF toi light01
light01 da TAT                            |         Nhap lenh:
Da gui trang thai:                        |         Trang thai nhan duoc:
{"device_id": "light01", "status": "OFF"} |         {"device_id": "light01", "status": "OFF"}     
     
-----------------------------------------
Thiet bi: fan01                           |         Nhap lenh: fan01 OFF
Nhan duoc lenh: OFF                       |         Da gui lenh OFF toi fan01
fan01 da TAT                              |         Nhap lenh:
Da gui trang thai:                        |         Trang thai nhan duoc:
{"device_id": "fan01", "status": "OFF"}   |         {"device_id": "fan01", "status": "OFF"}     