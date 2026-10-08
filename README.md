# Thực hành IoT với MQTT

Hướng dẫn chạy các bài thực hành Python MQTT và kết quả gửi nhận dữ liệu.

## Chuẩn bị môi trường

Mở PowerShell tại thư mục gốc `THUC_HANH_IOT`. Môi trường đã chạy thử Bài 1 và Bài 2: Python **3.11.9**, thư viện **paho-mqtt 2.1.0**. Phiên bản thư viện này hỗ trợ `CallbackAPIVersion.VERSION2`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install paho-mqtt==2.1.0
```

Chỉ cần tạo môi trường và cài thư viện lần đầu. Các lệnh dưới đây chạy từ thư mục gốc, không cần kích hoạt `.venv`.

## Broker MQTT

| Thông số | Giá trị |
| --- | --- |
| Broker | `broker.emqx.io` |
| Cổng | `1883` |
| Kết nối | MQTT TCP, không dùng TLS |
| Tài khoản | Không cấu hình username/password |

Broker là máy chủ trung gian: publisher gửi dữ liệu đến broker; broker chuyển tiếp đến subscriber đã đăng ký topic tương ứng.

## Bài 1: Gửi và nhận lời chào

Gửi lời chào từ publisher và nhận thông điệp bằng subscriber qua MQTT.

| Vai trò | File |
| --- | --- |
| Publisher | [publisher_bai1.py](Bai1/publisher_bai1.py) |
| Subscriber | [subscriber_bai1.py](Bai1/subscriber_bai1.py) |

Topic: `iot/lab/message`.

### Cách chạy

**Terminal 1 — chạy subscriber trước:**

```powershell
.\.venv\Scripts\python.exe -u .\Bai1\subscriber_bai1.py
```

Đợi xuất hiện `Dang lang nghe topic: iot/lab/message`.

**Terminal 2 — chạy publisher:**

```powershell
.\.venv\Scripts\python.exe -u .\Bai1\publisher_bai1.py
```

Publisher gửi một thông điệp rồi tự kết thúc. Subscriber tiếp tục lắng nghe; nhấn `Ctrl+C` để dừng.

### Kết quả chạy thực tế ngày 08/10/2026

**Terminal 2 — publisher:**

```text
Da gui message:
Xin chao tu client Python MQTT - B23DCC350 - Nguyen Doan Hop
```

**Terminal 1 — subscriber:**

```text
Ket noi MQTT broker thanh cong
Dang lang nghe topic: iot/lab/message

Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCC350 - Nguyen Doan Hop
Time: 14:38:52
```

Publisher gửi thành công, subscriber nhận đúng topic và payload. `Time` là giờ trên máy chạy subscriber lúc nhận thông điệp và sẽ thay đổi ở những lần chạy khác.

## Bài 2: Mô phỏng cảm biến và cảnh báo

Cảm biến `sensor01` gửi dữ liệu nhiệt độ và độ ẩm dạng JSON mỗi **3 giây**.

| Vai trò | File |
| --- | --- |
| Sensor publisher | [sensor_publisher_bai2.py](Bai2/sensor_publisher_bai2.py) |
| Monitor subscriber | [monitor_subscriber_bai2.py](Bai2/monitor_subscriber_bai2.py) |

Topic: `iot/lab/sensor01/data`.

### Dữ liệu và điều kiện cảnh báo

| Trường | Giá trị |
| --- | --- |
| `device_id` | `sensor01` |
| `temperature` | Ngẫu nhiên từ 25 đến 40 °C, làm tròn 1 chữ số thập phân |
| `humidity` | Ngẫu nhiên từ 30 đến 80 %, làm tròn 1 chữ số thập phân |

| Điều kiện | Thông báo |
| --- | --- |
| `temperature > 35` | `CANH BAO: Nhiet do cao` |
| `humidity < 40` | `CANH BAO: Do am thap` |

Hai điều kiện được kiểm tra riêng; có thể xuất hiện cả hai cảnh báo. Nhiệt độ bằng 35 hoặc độ ẩm bằng 40 không kích hoạt cảnh báo tương ứng.

### Cách chạy

**Terminal 1 — chạy monitor trước:**

```powershell
.\.venv\Scripts\python.exe -u .\Bai2\monitor_subscriber_bai2.py
```

Đợi xuất hiện `Dang lang nghe topic: iot/lab/sensor01/data`.

**Terminal 2 — chạy sensor publisher:**

```powershell
.\.venv\Scripts\python.exe -u .\Bai2\sensor_publisher_bai2.py
```

Hai chương trình chạy liên tục. Nhấn `Ctrl+C` ở mỗi terminal để dừng.

### Kết quả chạy thực tế ngày 08/10/2026

**Monitor khi kết nối:**

```text
Ket noi MQTT broker thanh cong
Dang lang nghe topic: iot/lab/sensor01/data
```

**Mẫu 1 — dữ liệu bình thường:**

Terminal 2:

```text
Da gui:
{"device_id": "sensor01", "temperature": 34.6, "humidity": 69.4}
```

Terminal 1:

```text
------------------------
Device: sensor01
Temperature: 34.6 C
Humidity: 69.4 %
```

**Mẫu 2 — độ ẩm thấp:**

Terminal 2:

```text
Da gui:
{"device_id": "sensor01", "temperature": 32.9, "humidity": 30.9}
```

Terminal 1:

```text
------------------------
Device: sensor01
Temperature: 32.9 C
Humidity: 30.9 %
CANH BAO: Do am thap
```

**Mẫu 3 — nhiệt độ cao:**

Terminal 2:

```text
Da gui:
{"device_id": "sensor01", "temperature": 36.5, "humidity": 45.4}
```

Terminal 1:

```text
------------------------
Device: sensor01
Temperature: 36.5 C
Humidity: 45.4 %
CANH BAO: Nhiet do cao
```

Monitor nhận đúng dữ liệu JSON do sensor publisher gửi; đã quan sát được cả cảnh báo nhiệt độ cao và cảnh báo độ ẩm thấp. Các giá trị được tạo ngẫu nhiên nên sẽ khác ở những lần chạy khác.

## Bài 3: Điều khiển thiết bị

Phần này chuyển từ nội dung Bài 3 đã có trong `README.txt`; Bài 3 không được chạy lại trong lần kiểm tra Bài 1 và Bài 2.

Sử dụng broker MQTT ở phần cấu hình chung. Thiết bị và controller kết nối qua broker.

### Cách chạy

**Terminal 1 — mô phỏng thiết bị:**

```powershell
.\.venv\Scripts\python.exe -u .\Bai3\device_bai3.py
```

**Terminal 2 — controller:**

```powershell
.\.venv\Scripts\python.exe -u .\Bai3\controller_bai3.py
```

```text
Thiet bi: light01, fan01, pump01
Cu phap: ON | OFF | <thiet bi> ON | <thiet bi> OFF | EXIT
Nhap lenh:
```

Nhập lệnh tại controller để bật hoặc tắt thiết bị.

### Kết quả đã ghi trong README.txt

```text
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
```

Bản ghi dạng văn bản: [README.txt](README.txt).
