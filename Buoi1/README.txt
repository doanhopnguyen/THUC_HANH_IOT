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